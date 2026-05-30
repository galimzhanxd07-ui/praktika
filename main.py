# main.py
import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.settings import BOT_TOKEN
from handlers.chat import router
from handlers.ollama_handler import router as ollama_router
from handlers.media_handler import router as media_router
from handlers.mcp_handler import router as mcp_router
from middlewares.rate_limit import RateLimitMiddleware

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# BOT
bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()
dp.message.middleware(
    RateLimitMiddleware()
)

# Router қосу
dp.include_router(mcp_router)      # ← сначала mcp
dp.include_router(ollama_router)   # ← потом ollama
dp.include_router(media_router)    # ← потом media
dp.include_router(router)          # ← chat в конце

async def main():
    print("🚀 BOT ІСКЕ ҚОСЫЛДЫ")
    await bot.delete_webhook(
        drop_pending_updates=True
    )
    await dp.start_polling(bot)

# RUN
if __name__ == "__main__":
    asyncio.run(main())