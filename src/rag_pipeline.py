import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_gigachat import GigaChat
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Правильные пути относительно корня проекта
PROJECT_ROOT = Path(__file__).parent.parent
PERSIST_DIR = PROJECT_ROOT / "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def get_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    vectorstore = Chroma(
        persist_directory=str(PERSIST_DIR),
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    return retriever


def format_docs(docs):
    return "\n\n".join(
        f"Источник: {doc.metadata.get('source', 'неизвестно')}\n{doc.page_content}"
        for doc in docs
    )


def create_rag_chain():
    retriever = get_retriever()

    prompt = ChatPromptTemplate.from_template("""
Ты — умный и точный помощник сотрудника банка.
Твоя задача — отвечать на вопросы строго на основе предоставленного контекста из внутренних документов.

Строгие правила:
1. Отвечай только на русском языке.
2. Если в контексте нет ответа — честно напиши: «В предоставленных документах информации по этому вопросу нет.»
3. В конце ответа обязательно укажи источники (названия файлов).
4. Никогда не придумывай информацию, которой нет в контексте.
5. Отвечай кратко, четко и по делу.

Контекст из документов банка:
{context}

Вопрос сотрудника: {question}

Ответ:
""")

    llm = GigaChat(
        credentials=os.getenv("GIGACHAT_CREDENTIALS"),
        scope=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
        model="GigaChat-2",
        verify_ssl_certs=False,
        temperature=0.1,
        top_p=0.3,
    )

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask(question: str) -> str:
    chain = create_rag_chain()
    return chain.invoke(question)