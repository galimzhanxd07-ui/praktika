# services/voice_service.py
import os
import tempfile
from groq import AsyncGroq
from config.settings import settings

groq = AsyncGroq(api_key=settings.GROQ_API_KEY)
async def transcribe_voice(file_path: str) -> str:
    with open(file_path, "rb") as f:
        transcription = await groq.audio.transcriptions.create(
            file=(os.path.basename(file_path), f),
            model="whisper-large-v3",
            language="ru"
        )
    return transcription.text

async def process_voice(bot, file_id: str) -> str:
    # Скачиваем файл
    file = await bot.get_file(file_id)
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        tmp_path = tmp.name
    await bot.download_file(file.file_path, tmp_path)

    # Проверяем размер (макс 25 МБ)
    size = os.path.getsize(tmp_path)
    if size > 25 * 1024 * 1024:
        os.unlink(tmp_path)
        return "Голосовое сообщение слишком длинное (макс 25 МБ)"

    try:
        text = await transcribe_voice(tmp_path)
        return text
    finally:
        os.unlink(tmp_path)