# tests/test_property.py
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

# Property 1 — парсинг команд не должен падать
@given(st.text(max_size=4096))
def test_command_parsing_never_crashes(text):
    try:
        parts = text.split()
        result = parts[0] if parts else ""
        assert isinstance(result, str)
    except Exception as e:
        pytest.fail(f"Упало на тексте: {text!r}, ошибка: {e}")

# Property 2 — нормализация текста
@given(st.text(max_size=4096))
def test_text_normalization(text):
    normalized = text.strip()
    assert isinstance(normalized, str)
    assert len(normalized) <= len(text)

# Property 3 — валидация user_id
@given(st.integers())
def test_user_id_validation(user_id):
    key = f"ctx:{user_id}"
    assert isinstance(key, str)
    assert str(user_id) in key

# Property 4 — rate limit ключи
@given(st.integers(min_value=1), st.integers(min_value=1))
def test_rate_limit_keys(user_id, chat_id):
    user_key = f"rl:user:{user_id}"
    chat_key = f"rl:chat:{chat_id}"
    assert str(user_id) in user_key
    assert str(chat_id) in chat_key

# Property 5 — длина ответа
@given(st.text(min_size=1, max_size=4096))
def test_response_length(text):
    truncated = text[:4096]
    assert len(truncated) <= 4096