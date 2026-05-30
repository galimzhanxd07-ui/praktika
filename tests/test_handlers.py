# tests/test_handlers.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Тест 1 — /start команда
@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    message.from_user.first_name = "Алибек"

    from handlers.chat import start_handler
    await start_handler(message)

    message.answer.assert_called_once()

# Тест 2 — rate limiter
@pytest.mark.asyncio
async def test_rate_limit_allows():
    from utils.rate_limiter import check_rate_limit
    result = await check_rate_limit(123, 456)
    assert result is True

# Тест 3 — groq service
@pytest.mark.asyncio
async def test_stream_response():
    with patch("services.groq_service.async_client") as mock_client:
        mock_chunk = MagicMock()
        mock_chunk.choices[0].delta.content = "Привет"

        async def mock_stream(*args, **kwargs):
            yield mock_chunk

        mock_client.chat.completions.create = AsyncMock(
            return_value=mock_stream()
        )

        from services.groq_service import stream_response
        chunks = []

        async def collect(t):
            chunks.append(t)

        result = await stream_response(
            [{"role": "user", "content": "тест"}],
            collect
        )
        assert "Привет" in result

# Тест 4 — context service
@pytest.mark.asyncio
async def test_get_history_empty():
    with patch("services.context_service.redis") as mock_redis:
        mock_redis.get = AsyncMock(return_value=None)
        from services.context_service import get_history
        history = await get_history(999)
        assert isinstance(history, list)
        assert len(history) >= 1

# Тест 5 — голосовое сообщение большой размер
@pytest.mark.asyncio
async def test_voice_too_large():
    import os
    with patch.object(os.path, "getsize", return_value=30 * 1024 * 1024):
        mock_bot = AsyncMock()
        mock_bot.get_file = AsyncMock(
            return_value=AsyncMock(file_path="test.ogg")
        )
        mock_bot.download_file = AsyncMock()

        from services.voice_service import process_voice
        result = await process_voice(mock_bot, "fake_id")
        assert "слишком" in result.lower() or "25" in result