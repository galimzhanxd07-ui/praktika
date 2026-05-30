import time
from groq import Groq, AsyncGroq
from config.settings import GROQ_API_KEY, settings

client = Groq(api_key=GROQ_API_KEY)
async_client = AsyncGroq(api_key=GROQ_API_KEY)

# Обновленная старая функция (для тестов и простых запросов)
def get_ai_response(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "Сен қазақ және орыс тілдерінде өте толық жауап беретін кәсіби AI көмекшісің. "
                    "Ты — профессиональный, эрудированный ИИ-ассистент. Твоя задача — давать "
                    "максимально подробные, логичные, развернутые и структурированные ответы. "
                    "Если тебя спрашивают про термины (например, ИИ, Python), давай детальное "
                    "определение, структуру, сферы применения и примеры. "
                    "Отвечай на том же языке, на котором задан вопрос."
                )
            },
            {"role": "user", "content": text}
        ],
        temperature=0.5,      # Сделали ответы более точными и академичными
        max_tokens=2000,      # Увеличили лимит токенов, чтобы ответ не обрывался
        stream=True
    )
    full_answer = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            full_answer += content
    return full_answer

# Новая функция для стриминга (без изменений, она написана отлично)
async def stream_response(messages: list, on_chunk) -> str:
    full_text = ""
    last_edit = 0.0

    try:
        stream = await async_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            stream=True,
            timeout=30,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full_text += delta
            now = time.monotonic()
            if now - last_edit >= 1.5:
                await on_chunk(full_text)
                last_edit = now

        await on_chunk(full_text)
    except Exception:
        raise

    return full_text