from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# ====================== НАСТРОЙКИ ======================
# Определяем корень проекта правильно
PROJECT_ROOT = Path(__file__).parent.parent          # поднимаемся из src/ на уровень выше
DATA_DIR = PROJECT_ROOT / "data"
PERSIST_DIR = PROJECT_ROOT / "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_documents() -> list[Document]:
    """Загружаем все .txt файлы из папки data"""
    documents = []

    print(f"Ищем документы в: {DATA_DIR}")

    if not DATA_DIR.exists():
        print(f"ОШИБКА: папка {DATA_DIR} не существует!")
        return documents

    txt_files = list(DATA_DIR.glob("**/*.txt"))
    print(f"Найдено .txt файлов: {len(txt_files)}")

    for file_path in txt_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            doc = Document(
                page_content=text,
                metadata={"source": str(file_path.name)}   # сохраняем только имя файла
            )
            documents.append(doc)
            print(f"  → Загружен: {file_path.name}")
        except Exception as e:
            print(f"  × Ошибка при чтении {file_path.name}: {e}")

    print(f"Всего загружено документов: {len(documents)}")
    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    """Режем документы на чанки"""
    if not documents:
        print("Нет документов для разбиения")
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Получено чанков: {len(chunks)}")
    return chunks


def create_vector_store(chunks: list[Document]):
    """Создаём векторную базу"""
    if not chunks:
        print("Нет чанков — векторная база не создана")
        return None

    print("Создаём эмбеддинги (подождите 20-60 секунд)...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(PERSIST_DIR)
    )

    print(f"Векторная база сохранена в: {PERSIST_DIR}")
    return vectorstore


if __name__ == "__main__":
    print("=" * 50)
    print("НАЧИНАЕМ ИНДЕКСАЦИЮ ДОКУМЕНТОВ")
    print("=" * 50)

    documents = load_documents()
    chunks = split_documents(documents)
    create_vector_store(chunks)

    print("=" * 50)
    print("ИНДЕКСАЦИЯ ЗАВЕРШЕНА")
    print("=" * 50)