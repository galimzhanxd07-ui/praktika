# services/context_service.py
import json
import redis.asyncio as aioredis
import tiktoken
from groq import AsyncGroq
from config.settings import settings

redis = aioredis.from_url(settings.redis_url, decode_responses=True)
groq = AsyncGroq(api_key=settings.GROQ_API_KEY)

SYSTEM = {"role": "system", "content": "Сен NovaBot — ақылды AI көмекшісі. Қазақша, орысша және ағылшынша жауап бер."}
MAX_TOKENS = 8000
encoder = tiktoken.get_encoding("cl100k_base")

def count_tokens(messages: list) -> int:
    total = 0
    for m in messages:
        total += len(encoder.encode(m.get("content", "")))
    return total

async def get_history(user_id: int) -> list:
    raw = await redis.get(f"ctx:{user_id}")
    messages = json.loads(raw) if raw else []
    return [SYSTEM] + messages

async def save_message(user_id: int, role: str, content: str):
    raw = await redis.get(f"ctx:{user_id}")
    messages = json.loads(raw) if raw else []
    messages.append({"role": role, "content": content})

    # Токен санын тексер
    total = count_tokens(messages)
    print(f"[Context] user={user_id} tokens={total}/{MAX_TOKENS} messages={len(messages)}")

    if total > MAX_TOKENS:
        print(f"[Context] Суммаризация басталды...")
        messages = await _summarize(messages)

    await redis.set(f"ctx:{user_id}", json.dumps(messages, ensure_ascii=False), ex=86400)

async def _summarize(messages: list) -> list:
    # Соңғы 10 хабарды қалдырып, қалғанын суммаризациялаймыз
    old = messages[:-10]
    recent = messages[-10:]

    text = "\n".join(f"{m['role']}: {m['content']}" for m in old)

    resp = await groq.chat.completions.create(
        model=settings.groq_model_fast,
        messages=[
            {"role": "system", "content": "Осы диалогты 3-5 сөйлеммен қысқаша суммаризациялаңыз. Маңызды ақпаратты сақтаңыз."},
            {"role": "user", "content": text},
        ],
        max_tokens=500,
    )
    summary = resp.choices[0].message.content
    print(f"[Context] Суммаризация дайын: {summary[:100]}...")

    return [
        {"role": "system", "content": f"Алдыңғы диалогтың қысқаша мазмұны: {summary}"}
    ] + recent

async def clear_history(user_id: int):
    await redis.delete(f"ctx:{user_id}")
    print(f"[Context] user={user_id} история очищена")