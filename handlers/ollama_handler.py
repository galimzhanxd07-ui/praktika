# handlers/ollama_handler.py
import asyncio
import ollama
from aiogram import Router, types
from aiogram.filters import Command
from services.ollama_service import toggle_private, is_private_mode

router = Router()

# ==========================
# /private команда (Задача 13)
# ==========================
@router.message(Command("private"))
async def cmd_private(message: types.Message):
    uid = message.from_user.id
    is_on = await toggle_private(uid)

    if is_on:
        await message.answer(
            "🔒 Приватный режим включён\n"
            "Все сообщения обрабатываются локально через Ollama\n"
            "Данные не уходят в облако"
        )
    else:
        await message.answer(
            "☁️ Обычный режим включён\n"
            "Сообщения обрабатываются через Groq AI"
        )

# ==========================
# /benchmark команда (Задача 15)
# ==========================
@router.message(Command("benchmark"))
async def cmd_benchmark(message: types.Message):
    sent = await message.answer("Запускаю бенчмарк...")
    from services.benchmark_service import run_benchmark
    result = await run_benchmark()
    await sent.edit_text(result)

# ==========================
# /model команда (Задача 17)
# ==========================
@router.message(Command("model"))
async def cmd_model(message: types.Message):
    args = message.text.split()

    if len(args) < 3 or args[1] != "pull":
        await message.answer(
            "Использование: /model pull <название>\n"
            "Пример: /model pull llama3.2:3b"
        )
        return

    model_name = args[2]
    sent = await message.answer(f"Начинаю загрузку модели {model_name}...")

    try:
        for i in range(1, 6):
            await asyncio.sleep(5)
            try:
                await sent.edit_text(
                    f"⏳ Загрузка {model_name}...\n"
                    f"Прошло: {i * 5} секунд"
                )
            except Exception:
                pass

        ollama.pull(model_name)
        await sent.edit_text(f"✅ Модель {model_name} успешно загружена!")

    except Exception as e:
        if "no space left" in str(e).lower():
            await sent.edit_text("❌ Недостаточно места на диске!")
        elif "connection" in str(e).lower():
            await sent.edit_text("❌ Ошибка сети при загрузке!")
        else:
            await sent.edit_text(f"❌ Ошибка загрузки: {e}")
@router.message(Command("tools"))
async def cmd_tools(message: types.Message):
    sent = await message.answer("Тестирую function calling...")
    from services.ollama_tools_service import run_tool_comparison
    result = await run_tool_comparison()
    await sent.edit_text(result)