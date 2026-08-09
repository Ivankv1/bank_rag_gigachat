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

Структура проекта:
bank_rag_gigachat/
├── data/                  
├── src/
│   ├── ingest.py          
│   ├── rag_pipeline.py    
│   └── evaluate.py        
├── app.py                 
├── requirements.txt
└── README.md
