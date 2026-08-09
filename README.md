**Умный помощник по внутренним регламентам банка** на базе GigaChat и технологии RAG.


[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![GigaChat](https://img.shields.io/badge/LLM-GigaChat--2-green.svg)](https://developers.sber.ru/gigachat)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-orange.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Описание проекта

Система позволяет сотрудникам банка быстро получать точные ответы на вопросы по внутренним документам:

- Кредитная политика
- Правила AML (противодействие отмыванию доходов)
- Процедуры KYC (идентификация клиентов)

Ответы генерируются **только** на основе загруженных документов с обязательным указанием источников. Это снижает риск галлюцинаций и повышает доверие к системе.

---

## Ключевые возможности

- Семантический поиск по внутренним регламентам
- Генерация ответов через **GigaChat-2**
- Обязательное указание источников
- Честный отказ, если информации в документах нет
- Простой веб-интерфейс на Streamlit
- Набор автотестов качества (6/6 = 100%)

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
