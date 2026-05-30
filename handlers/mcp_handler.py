# handlers/mcp_handler.py
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("resources"))
async def cmd_resources(message: types.Message):
    await message.answer(
        "📚 Доступные ресурсы:\n"
        "• file://templates/report — Шаблон отчёта\n"
        "• file://templates/letter — Шаблон письма"
    )

@router.message(Command("prompts"))
async def cmd_prompts(message: types.Message):
    await message.answer(
        "📝 Доступные промпты:\n"
        "• summarize — суммаризация текста\n"
        "• translate_kz — перевод на казахский"
    )

@router.message(Command("files"))
async def cmd_files(message: types.Message):
    try:
        from services.mcp_client import aggregator
        result = await aggregator.call_tool("fs__list_files", {})
        await message.answer(f"📁 Файлы:\n{result}")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    try:
        from services.mcp_client import aggregator
        result = await aggregator.call_tool("pg__get_user_stats", {})
        await message.answer(result)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")