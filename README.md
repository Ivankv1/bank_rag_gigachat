# Bank Policies RAG Assistant

Умный помощник по внутренним регламентам банка на базе **GigaChat** и технологии **RAG** (Retrieval-Augmented Generation).

## Возможности

- Ответы на вопросы по внутренним документам банка (кредитная политика, AML, KYC)
- Поиск релевантных фрагментов документов по смыслу
- Генерация ответов строго на основе найденного контекста
- Указание источников
- Веб-интерфейс на Streamlit

## Архитектура

Документы (TXT)
↓
Chunking (RecursiveCharacterTextSplitter)
↓
Embeddings (sentence-transformers multilingual)
↓
Vector Store (ChromaDB)
↓
Retriever (top-k = 4)
↓
Prompt + Context
↓
GigaChat-2
↓
Ответ + источники

## Технологический стек

- **LLM**: GigaChat-2 (Sber)
- **Framework**: LangChain + langchain-gigachat
- **Embeddings**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Vector DB**: ChromaDB
- **UI**: Streamlit
- **Language**: Python 3.11+

## Быстрый старт

1. Клонируйте репозиторий
2. Создайте виртуальное окружение и установите зависимости:
pip install -r requirements.txt
3.Создайте файл .env и укажите ключ
GigaChat:envGIGACHAT_CREDENTIALS=ваш_ключ
GIGACHAT_SCOPE=GIGACHAT_API_PERS

4.Проиндексируйте документы:
python -m src.ingest
5. Запустите интерфейс:
streamlit run app.py

Структура проекта:
bank_rag_gigachat/
├── data/                  # Внутренние документы банка
├── src/
│   ├── ingest.py          # Индексация документов
│   ├── rag_pipeline.py    # RAG-пайплайн
│   └── evaluate.py        # Простая оценка качества
├── app.py                 # Streamlit-интерфейс
├── requirements.txt
└── README.md