# services/ollama_tools_service.py
import ollama
import json
import time
from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Получить погоду в городе",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Название города"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Вычислить математическое выражение",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Математическое выражение"}
                },
                "required": ["expression"]
            }
        }
    }
]

def get_weather(city: str) -> str:
    return f"Погода в {city}: 20°C, ясно"

def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return f"Результат: {result}"
    except Exception:
        return "Ошибка вычисления"

TEST_CASES = [
    "Какая погода в Алматы?",
    "Посчитай 2 + 2",
    "Погода в Астане сегодня",
    "Вычисли 10 * 5",
    "Какая погода в Москве?",
]

def test_ollama_tools(question: str) -> dict:
    start = time.monotonic()
    errors = []
    result = "нет ответа"

    try:
        response = ollama.chat(
            model="llama3.1",
            messages=[{"role": "user", "content": question}],
            tools=TOOLS
        )
        msg = response["message"]
        elapsed = time.monotonic() - start

        if msg.get("tool_calls"):
            tool_call = msg["tool_calls"][0]
            name = tool_call["function"]["name"]
            try:
                args = tool_call["function"]["arguments"]
                if isinstance(args, str):
                    args = json.loads(args)
                if name == "get_weather":
                    result = get_weather(args["city"])
                elif name == "calculate":
                    result = calculate(args["expression"])
            except json.JSONDecodeError as e:
                errors.append(f"JSON ошибка: {e}")
                result = "ошибка парсинга JSON"
        else:
            result = msg["content"]

    except Exception as e:
        elapsed = time.monotonic() - start
        errors.append(str(e))

    return {
        "question": question,
        "result": result,
        "latency": elapsed,
        "errors": errors,
        "success": len(errors) == 0
    }

def test_groq_tools(question: str) -> dict:
    start = time.monotonic()
    errors = []
    result = "нет ответа"

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": question}],
            tools=TOOLS,
            tool_choice="auto"
        )
        msg = response.choices[0].message
        elapsed = time.monotonic() - start

        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            name = tool_call.function.name
            try:
                args = json.loads(tool_call.function.arguments)
                if name == "get_weather":
                    result = get_weather(args["city"])
                elif name == "calculate":
                    result = calculate(args["expression"])
            except json.JSONDecodeError as e:
                errors.append(f"JSON ошибка: {e}")
                result = "ошибка парсинга JSON"
        else:
            result = msg.content

    except Exception as e:
        elapsed = time.monotonic() - start
        errors.append(str(e))

    return {
        "question": question,
        "result": result,
        "latency": elapsed,
        "errors": errors,
        "success": len(errors) == 0
    }

async def run_tool_comparison() -> str:
    ollama_results = []
    groq_results = []
    ollama_errors = []

    for q in TEST_CASES:
        o = test_ollama_tools(q)
        g = test_groq_tools(q)
        ollama_results.append(o)
        groq_results.append(g)
        if o["errors"]:
            ollama_errors.extend(o["errors"])

    ollama_success = sum(1 for r in ollama_results if r["success"])
    groq_success = sum(1 for r in groq_results if r["success"])

    report = (
        f"🔧 Function calling нәтижелері:\n\n"
        f"🖥 Ollama: {ollama_success}/{len(TEST_CASES)} сәтті\n"
        f"⚡ Groq: {groq_success}/{len(TEST_CASES)} сәтті\n\n"
    )

    if ollama_errors:
        report += "❌ Ollama қателері:\n"
        for e in ollama_errors[:3]:
            report += f"• {e}\n"

    return report