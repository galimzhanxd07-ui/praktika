# webhook.py
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from config.settings import settings
from handlers.chat import router
from handlers.ollama_handler import router as ollama_router
from handlers.media_handler import router as media_router

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://vastly-reformed-variably.ngrok-free.dev/webhook"
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    print("Webhook удалён")

def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    dp.include_router(ollama_router)
    dp.include_router(media_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    handler.register(app, path=WEBHOOK_PATH)

    web.run_app(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()