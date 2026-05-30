# middlewares/rate_limit.py
import time
from aiogram import BaseMiddleware
from aiogram.types import Message

user_last_message = {}

class RateLimitMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        user_id = event.from_user.id
        now = time.time()

        if user_id in user_last_message:
            last_time = user_last_message[user_id]
            if now - last_time < 3:
                await event.answer(
                    "⏳ Тым жиі сұраныс жібердіңіз. "
                    "3 секунд күтіңіз."
                )
                return

        user_last_message[user_id] = now
        return await handler(event, data)

# Функция для chat_handler
async def check_rate_limit(user_id: int, chat_id: int) -> bool:
    now = time.time()
    if user_id in user_last_message:
        if now - user_last_message[user_id] < 3:
            return False
    user_last_message[user_id] = now
    return True