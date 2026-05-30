# services/ollama_service.py
import ollama
import redis.asyncio as aioredis
from config.settings import settings

redis = aioredis.from_url(settings.redis_url, decode_responses=True)

async def is_private_mode(user_id: int) -> bool:
    val = await redis.get(f"private:{user_id}")
    return val == "1"

async def toggle_private(user_id: int) -> bool:
    current = await is_private_mode(user_id)
    new_val = "0" if current else "1"
    await redis.set(f"private:{user_id}", new_val)
    return not current

async def ollama_chat(messages: list) -> str:
    response = ollama.chat(
        model="llama3.2:3b",
        messages=messages
    )
    return response["message"]["content"]