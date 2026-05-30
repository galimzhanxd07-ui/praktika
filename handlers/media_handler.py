# handlers/media_handler.py
import tempfile
import os
from aiogram import Router, types, Bot
from aiogram.filters import Command
from services.voice_service import process_voice
from services.search_service import search_web
from services.image_service import analyze_image

router = Router()

# ==========================
# Задача 18 — Голосовые
# ==========================
@router.message(lambda m: m.voice is not None)
async def handle_voice(message: types.Message, bot: Bot):
    sent = await message.answer("Распознаю голосовое сообщение...")
    try:
        # Распознаём голос
        text = await process_voice(bot, message.voice.file_id)
        await sent.edit_text(f"🎤 Распознано: {text}\n\n⏳ Думаю...")

        # Отправляем в Groq
        from services.groq_service import stream_response
        history = [
            {"role": "system", "content": "Ты вежливый помощник студента."},
            {"role": "user", "content": text}
        ]

        async def update(reply_text: str):
            try:
                await sent.edit_text(
                    f"🎤 Распознано: {text}\n\n💬 {reply_text}"
                )
            except Exception:
                pass

        await stream_response(history, update)

    except Exception as e:
        await sent.edit_text(f"Ошибка распознавания: {e}")

# ==========================
# Задача 19 — Поиск
# ==========================
@router.message(Command("search"))
async def handle_search(message: types.Message):
    query = message.text.replace("/search", "").strip()
    if not query:
        await message.answer("Использование: /search <запрос>")
        return

    sent = await message.answer("Ищу в интернете...")
    try:
        results = await search_web(query)
        await sent.edit_text(f"🔍 Результаты:\n\n{results}")
    except Exception as e:
        await sent.edit_text(f"Ошибка поиска: {e}")

# ==========================
# Задача 20 — Изображения
# ==========================
@router.message(lambda m: m.photo is not None)
async def handle_photo(message: types.Message, bot: Bot):
    sent = await message.answer("Анализирую изображение...")
    try:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name
        await bot.download_file(file.file_path, tmp_path)

        description = await analyze_image(tmp_path)
        os.unlink(tmp_path)

        await sent.edit_text(f"🖼 Описание:\n{description}")
    except Exception as e:
        await sent.edit_text(f"Ошибка анализа: {e}")

# ==========================
# Задача 21 — Google Calendar
# ==========================
@router.message(Command("calendar"))
async def handle_calendar(message: types.Message):
    await message.answer(
        "📅 Google Calendar\n\n"
        "Для привязки аккаунта обратитесь к администратору.\n"
        "Использование: /event <название> <дата>\n"
        "Пример: /event Встреча 2026-05-27T14:00:00"
    )

@router.message(Command("event"))
async def handle_event(message: types.Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer(
            "Использование: /event <название> <дата>\n"
            "Пример: /event Встреча 2026-05-27T14:00:00"
        )
        return

    title = args[1]
    datetime_str = args[2]
    uid = message.from_user.id

    from services.calendar_service import create_event
    result = await create_event(uid, title, datetime_str)
    await message.answer(result)