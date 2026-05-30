# benchmark_rag.py
import asyncio
import time
from services.rag_service import ask_with_rag

questions = [
    "Что такое Python?",
    "Как работает Docker?",
    "Что такое машинное обучение?",
    "Расскажи про Redis",
    "Что такое REST API?",
]

async def main():
    times = []
    for q in questions:
        start = time.monotonic()
        answer = await ask_with_rag(q)
        elapsed = time.monotonic() - start
        times.append(elapsed)
        print(f"Вопрос: {q}")
        print(f"Время: {elapsed:.2f}с")
        print(f"Ответ: {answer[:100]}...")
        print()

    avg = sum(times) / len(times)
    print(f"Среднее время: {avg:.2f}с")

asyncio.run(main())