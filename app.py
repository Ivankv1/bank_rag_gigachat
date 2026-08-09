import streamlit as st
from src.rag_pipeline import ask

# ====================== НАСТРОЙКИ СТРАНИЦЫ ======================
st.set_page_config(
    page_title="Bank RAG Assistant | GigaChat",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ====================== СТИЛИ ======================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 600;
    }
    .source-box {
        background-color: #f0f7ff;
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 4px solid #1e88e5;
        margin-top: 1rem;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ====================== БОКОВАЯ ПАНЕЛЬ ======================
with st.sidebar:
    st.header("О проекте")
    st.markdown("""
    **Bank Policies RAG Assistant**

    Умный помощник по внутренним регламентам банка на базе:
    - **GigaChat-2**
    - **RAG** (Retrieval-Augmented Generation)
    - **ChromaDB** + multilingual embeddings

    Проект создан для портфолио Data Scientist.
    """)

    st.divider()
    st.markdown("**Технологии:**")
    st.markdown("- LangChain + LangChain-GigaChat")
    st.markdown("- HuggingFace Embeddings")
    st.markdown("- Streamlit")
    st.markdown("- Chroma Vector Store")

# ====================== ОСНОВНАЯ ЧАСТЬ ======================
st.markdown('<div class="main-title">🏦 Bank Policies RAG Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Помощник по внутренним регламентам банка на GigaChat</div>', unsafe_allow_html=True)

# Примеры вопросов в виде кнопок
st.markdown("#### Примеры вопросов")
col1, col2 = st.columns(2)

examples = [
    "Какая максимальная сумма потребительского кредита?",
    "Нужно ли отправлять сообщение при операции на 700 000 рублей?",
    "Какие документы нужны для открытия счёта физическому лицу?",
    "Есть ли комиссия при досрочном погашении?",
    "Какой минимальный первоначальный взнос по ипотеке?",
    "Какой максимальный срок потребительского кредита?"
]

selected_example = None
with col1:
    if st.button(examples[0]):
        selected_example = examples[0]
    if st.button(examples[2]):
        selected_example = examples[2]
    if st.button(examples[4]):
        selected_example = examples[4]

with col2:
    if st.button(examples[1]):
        selected_example = examples[1]
    if st.button(examples[3]):
        selected_example = examples[3]
    if st.button(examples[5]):
        selected_example = examples[5]

st.divider()

# Поле ввода
question = st.text_input(
    "Ваш вопрос:",
    value=selected_example if selected_example else "",
    placeholder="Введите вопрос по регламентам банка..."
)

# Кнопка отправки
if st.button("Получить ответ", type="primary"):
    if not question.strip():
        st.warning("Пожалуйста, введите вопрос")
    else:
        with st.spinner("Ищу информацию в документах и генерирую ответ через GigaChat..."):
            try:
                answer = ask(question)

                st.markdown("### Ответ")
                st.success(answer)

                # Дополнительный блок
                st.markdown("---")
                st.caption(
                    "Ответ сгенерирован моделью GigaChat-2 на основе внутренних документов банка с использованием RAG.")

            except Exception as e:
                st.error(f"Произошла ошибка:\n\n{e}")
