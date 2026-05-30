# utils/rate_limiter.py
import time

user_last_message = {}

async def check_rate_limit(user_id: int, chat_id: int) -> bool:
    now = time.time()
    if user_id in user_last_message:
        if now - user_last_message[user_id] < 3:
            return False
    user_last_message[user_id] = now
    return True