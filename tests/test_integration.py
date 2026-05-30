# tests/test_integration.py
import pytest
from unittest.mock import AsyncMock, patch

# Сценарий 1 — /start
@pytest.mark.asyncio
async def test_scenario_start():
    message = AsyncMock()
    message.from_user.first_name = "Тест"
    message.from_user.id = 12345

    from handlers.chat import start_handler
    await start_handler(message)
    assert message.answer.called
# Сценарий 2 — вопрос → ответ
@pytest.mark.asyncio
async def test_scenario_question():
    message = AsyncMock()
    message.text = "Что такое Python?"
    message.from_user.id = 12345
    message.chat.id = 12345

    with patch("middlewares.rate_limit.user_last_message", {}):
        with patch("services.ollama_service.is_private_mode", return_value=False):
            with patch("services.model_router.route_model", return_value="Python — язык программирования"):
                from handlers.chat import chat_handler
                await chat_handler(message)
                assert message.answer.called
# Сценарий 3 — rate limit
@pytest.mark.asyncio
async def test_scenario_rate_limit():
    message = AsyncMock()
    message.text = "тест"
    message.from_user.id = 77777
    message.chat.id = 77777

    import utils.rate_limiter as rl
    rl.user_last_message[77777] = 9999999999

    from handlers.chat import chat_handler
    await chat_handler(message)
    assert message.answer.called

    del rl.user_last_message[77777]

# Сценарий 4 — /help
@pytest.mark.asyncio
async def test_scenario_help():
    message = AsyncMock()
    from handlers.chat import help_handler
    await help_handler(message)
    assert message.answer.called

# Сценарий 5 — приватный режим
@pytest.mark.asyncio
async def test_scenario_private_mode():
    message = AsyncMock()
    message.from_user.id = 12345

    with patch("services.ollama_service.toggle_private", return_value=True):
        from handlers.ollama_handler import cmd_private
        await cmd_private(message)
        assert message.answer.called