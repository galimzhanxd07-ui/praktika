# services/context_service.py
import json
import redis.asyncio as aioredis
from groq import AsyncGroq
from config.settings import settings

redis = aioredis.from_url(settings.redis_url, decode_responses=True)
groq = AsyncGroq(api_key=settings.GROQ_API_KEY)

SYSTEM = {"role": "system", "content": "Ты вежливый помощник студента."}

async def get_history(user_id: int) -> list:
    raw = await redis.get(f"ctx:{user_id}")
    messages = json.loads(raw) if raw else []
    return [SYSTEM] + messages

async def save_message(user_id: int, role: str, content: str):
    raw = await redis.get(f"ctx:{user_id}")
    messages = json.loads(raw) if raw else []
    messages.append({"role": role, "content": content})

    # ~250 слов на сообщение → при >30 сообщениях суммаризируем
    if len(messages) > 30:
        messages = await _summarize(messages)

    await redis.set(f"ctx:{user_id}", json.dumps(messages), ex=86400)

async def _summarize(messages: list) -> list:
    old = messages[:-10]   # суммаризируем всё кроме последних 10
    recent = messages[-10:]

    text = "\n".join(f"{m['role']}: {m['content']}" for m in old)
    resp = await groq.chat.completions.create(
        model=settings.groq_model_fast,
        messages=[
            {"role": "system", "content": "Кратко суммаризируй этот диалог в 3–5 предложениях."},
            {"role": "user", "content": text},
        ],
    )
    summary = resp.choices[0].message.content
    return [{"role": "system", "content": f"Краткое содержание предыдущего диалога: {summary}"}] + recent