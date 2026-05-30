# services/benchmark_service.py
import time
import statistics
import psutil
import ollama
from groq import Groq
from config.settings import GROQ_API_KEY
import openpyxl
from openpyxl.styles import Font, PatternFill

client = Groq(api_key=GROQ_API_KEY)

QUESTIONS = [
    "Что такое Python?",
    "Объясни машинное обучение",
    "Что такое база данных?",
    "Как работает интернет?",
    "Что такое Docker?",
    "Объясни REST API",
    "Что такое Git?",
    "Как работает нейронная сеть?",
    "Что такое Redis?",
    "Объясни микросервисы",
    "Что такое Kubernetes?",
    "Как работает TCP/IP?",
    "Что такое SQL?",
    "Объясни ООП",
    "Что такое API?",
    "Как работает HTTP?",
    "Что такое Linux?",
    "Объясни алгоритмы сортировки",
    "Что такое облачные вычисления?",
    "Как работает шифрование?",
]

def test_groq(question: str) -> dict:
    start = time.monotonic()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": question}],
        max_tokens=100
    )
    elapsed = time.monotonic() - start
    tokens = response.usage.completion_tokens
    return {
        "latency": elapsed,
        "tokens": tokens,
        "tokens_per_sec": tokens / elapsed if elapsed > 0 else 0,
        "cost": tokens * 0.000001
    }

def test_ollama(question: str) -> dict:
    ram_before = psutil.virtual_memory().used
    start = time.monotonic()
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": question}]
    )
    elapsed = time.monotonic() - start
    ram_after = psutil.virtual_memory().used
    ram_used = (ram_after - ram_before) / 1024 / 1024
    content = response["message"]["content"]
    tokens = len(content.split())
    return {
        "latency": elapsed,
        "tokens": tokens,
        "tokens_per_sec": tokens / elapsed if elapsed > 0 else 0,
        "ram_mb": ram_used
    }

def save_excel(groq_results: list, ollama_results: list) -> str:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Benchmark"

    # Заголовки
    headers = ["Вопрос", "Groq latency", "Groq tokens/sec", "Groq стоимость",
               "Ollama latency", "Ollama tokens/sec", "Ollama RAM MB"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="4472C4")

    # Данные
    for i, (q, g, o) in enumerate(zip(QUESTIONS, groq_results, ollama_results), 2):
        ws.cell(row=i, column=1, value=q)
        ws.cell(row=i, column=2, value=round(g["latency"], 3))
        ws.cell(row=i, column=3, value=round(g["tokens_per_sec"], 1))
        ws.cell(row=i, column=4, value=round(g["cost"], 6))
        ws.cell(row=i, column=5, value=round(o["latency"], 3))
        ws.cell(row=i, column=6, value=round(o["tokens_per_sec"], 1))
        ws.cell(row=i, column=7, value=round(o["ram_mb"], 1))

    # Итоги
    row = len(QUESTIONS) + 3
    ws.cell(row=row, column=1, value="ИТОГО").font = Font(bold=True)

    groq_latencies = [r["latency"] for r in groq_results]
    ollama_latencies = [r["latency"] for r in ollama_results]

    ws.cell(row=row+1, column=1, value="p50 latency")
    ws.cell(row=row+1, column=2, value=round(statistics.median(groq_latencies), 3))
    ws.cell(row=row+1, column=5, value=round(statistics.median(ollama_latencies), 3))

    ws.cell(row=row+2, column=1, value="p95 latency")
    ws.cell(row=row+2, column=2, value=round(sorted(groq_latencies)[int(len(groq_latencies)*0.95)], 3))
    ws.cell(row=row+2, column=5, value=round(sorted(ollama_latencies)[int(len(ollama_latencies)*0.95)], 3))

    ws.cell(row=row+3, column=1, value="p99 latency")
    ws.cell(row=row+3, column=2, value=round(sorted(groq_latencies)[int(len(groq_latencies)*0.99)], 3))
    ws.cell(row=row+3, column=5, value=round(sorted(ollama_latencies)[int(len(ollama_latencies)*0.99)], 3))

    path = "benchmark_results.xlsx"
    wb.save(path)
    return path

async def run_benchmark() -> str:
    groq_results = []
    ollama_results = []

    for i, q in enumerate(QUESTIONS):
        try:
            g = test_groq(q)
            groq_results.append(g)
        except Exception as e:
            groq_results.append({"latency": 0, "tokens": 0, "tokens_per_sec": 0, "cost": 0})

        try:
            o = test_ollama(q)
            ollama_results.append(o)
        except Exception as e:
            ollama_results.append({"latency": 0, "tokens": 0, "tokens_per_sec": 0, "ram_mb": 0})

    path = save_excel(groq_results, ollama_results)

    groq_avg = sum(r["latency"] for r in groq_results) / len(groq_results)
    ollama_avg = sum(r["latency"] for r in ollama_results) / len(ollama_results)

    return (
        f"📊 Бенчмарк нәтижелері ({len(QUESTIONS)} сұрақ):\n\n"
        f"⚡ Groq орташа: {groq_avg:.2f}с\n"
        f"🖥 Ollama орташа: {ollama_avg:.2f}с\n\n"
        f"{'⚡ Groq жылдамырақ!' if groq_avg < ollama_avg else '🖥 Ollama жылдамырақ!'}\n\n"
        f"📁 Excel есеп сақталды: {path}"
    )