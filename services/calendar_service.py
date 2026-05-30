# services/calendar_service.py
import json
from cryptography.fernet import Fernet
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import redis.asyncio as aioredis
from config.settings import settings

redis = aioredis.from_url(settings.redis_url, decode_responses=True)
fernet = Fernet(settings.fernet_key.encode())

async def save_tokens(user_id: int, tokens: dict):
    encrypted = fernet.encrypt(json.dumps(tokens).encode()).decode()
    await redis.set(f"gcal:{user_id}", encrypted)

async def get_tokens(user_id: int) -> dict | None:
    raw = await redis.get(f"gcal:{user_id}")
    if not raw:
        return None
    return json.loads(fernet.decrypt(raw.encode()).decode())

async def create_event(user_id: int, title: str, datetime_str: str) -> str:
    tokens = await get_tokens(user_id)
    if not tokens:
        return "Сначала привяжите Google аккаунт через /calendar"

    creds = Credentials(token=tokens["access_token"])
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": title,
        "start": {"dateTime": datetime_str, "timeZone": "Asia/Almaty"},
        "end": {"dateTime": datetime_str, "timeZone": "Asia/Almaty"},
    }
    service.events().insert(calendarId="primary", body=event).execute()
    return f"Событие '{title}' создано на {datetime_str}"