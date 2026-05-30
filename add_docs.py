# add_docs.py
import asyncio
from services.rag_service import add_document

docs = [
    ("doc1", "Python — это язык программирования высокого уровня."),
    ("doc2", "Машинное обучение — это раздел искусственного интеллекта."),
    ("doc3", "Нейронные сети имитируют работу мозга человека."),
    ("doc4", "Django — это веб-фреймворк на Python."),
    ("doc5", "Redis — это база данных типа ключ-значение."),
    ("doc6", "PostgreSQL — это реляционная база данных."),
    ("doc7", "Docker — это платформа для контейнеризации."),
    ("doc8", "Git — это система контроля версий."),
    ("doc9", "REST API — это архитектурный стиль для веб-сервисов."),
    ("doc10", "Groq — это платформа для быстрого инференса LLM."),
]

async def main():
    for doc_id, text in docs:
        await add_document(doc_id, text)
        print(f"Добавлен: {doc_id}")
    print("Все документы добавлены!")

asyncio.run(main())