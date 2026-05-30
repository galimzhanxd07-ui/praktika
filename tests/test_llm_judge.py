# tests/test_llm_judge.py
import pytest
from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

QUESTIONS = [
    ("Что такое Python?", "Python — язык программирования"),
    ("Столица Казахстана?", "Астана"),
    ("2+2?", "4"),
]

def get_bot_answer(question: str) -> str:
    from services.groq_service import get_ai_response
    return get_ai_response(question)

def judge_answer(question: str, answer: str) -> int:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Оцени ответ от 1 до 10. Верни только цифру."
            },
            {
                "role": "user",
                "content": f"Вопрос: {question}\nОтвет: {answer}"
            }
        ]
    )
    try:
        return int(response.choices[0].message.content.strip())
    except Exception:
        return 5

def test_llm_judge():
    scores = []
    for question, _ in QUESTIONS:
        answer = get_bot_answer(question)
        score = judge_answer(question, answer)
        scores.append(score)
        print(f"Вопрос: {question}\nОценка: {score}/10\n")

    avg = sum(scores) / len(scores)
    print(f"Средняя оценка: {avg:.1f}/10")
    assert avg >= 6.0, f"Качество ответов низкое: {avg:.1f}/10"