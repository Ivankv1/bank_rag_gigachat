from src.rag_pipeline import ask

# Набор тестовых вопросов и ожидаемых ключевых фактов
TEST_CASES = [
    {
        "question": "Какая максимальная сумма потребительского кредита?",
        "must_contain": ["5 000 000", "5000000", "5 млн"]
    },
    {
        "question": "Нужно ли отправлять сообщение при операции на 700 000 рублей?",
        "must_contain": ["да", "обязательно", "600 000"]
    },
    {
        "question": "Какие документы нужны для открытия счёта физическому лицу?",
        "must_contain": ["паспорт", "инн"]
    },
    {
        "question": "Есть ли комиссия при досрочном погашении?",
        "must_contain": ["нет", "не взимаются", "комиссии не"]
    },
    {
        "question": "Какой максимальный срок потребительского кредита?",
        "must_contain": ["7 лет"]
    },
    {
        "question": "Какая процентная ставка по автокредиту?",  # информации нет
        "must_contain": ["нет", "отсутствует", "не найдено", "информации нет"]
    },
]


def evaluate():
    print("=" * 60)
    print("ОЦЕНКА КАЧЕСТВА RAG-СИСТЕМЫ")
    print("=" * 60)

    passed = 0
    total = len(TEST_CASES)

    for i, case in enumerate(TEST_CASES, 1):
        question = case["question"]
        must_contain = case["must_contain"]

        print(f"\n[{i}/{total}] Вопрос: {question}")

        try:
            answer = ask(question)
            answer_lower = answer.lower()

            # Проверяем, содержится ли хотя бы один ожидаемый факт
            found = any(keyword.lower() in answer_lower for keyword in must_contain)

            if found:
                print("Результат: PASSED")
                passed += 1
            else:
                print("Результат: FAILED")
                print(f"Ответ модели: {answer[:300]}...")
        except Exception as e:
            print(f"Результат: ERROR — {e}")

    print("\n" + "=" * 60)
    print(f"Итого: {passed}/{total} тестов пройдено ({passed / total * 100:.0f}%)")
    print("=" * 60)


if __name__ == "__main__":
    evaluate()