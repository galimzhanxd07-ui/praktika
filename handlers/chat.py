# handlers/chat.py
import logging
from aiogram import Router, types
from aiogram.filters import Command
from services.groq_service import get_ai_response
from services.model_router import route_model
from services.ollama_service import is_private_mode, ollama_chat
from utils.logger import get_logger, generate_request_id, get_tracer

router = Router()
log = get_logger(__name__)
tracer = get_tracer()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        f"Сәлем, {message.from_user.first_name}! 👋\n\n"
        "Мен қазақ тілінде жауап беретін AI ботпын."
    )

@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(
        "<b>Командалар:</b>\n\n"
        "🤖 <b>Негізгі:</b>\n"
        "/start - Ботты бастау\n"
        "/help - Командалар тізімі\n\n"
        "🔒 <b>Режимдер:</b>\n"
        "/private - Приватный режим\n\n"
        "🔍 <b>Іздеу:</b>\n"
        "/search - Интернеттен іздеу\n"
        "/ask - RAG іздеу\n\n"
        "📁 <b>MCP:</b>\n"
        "/files - Файлдарды көрсету\n"
        "/resources - Ресурстар\n"
        "/prompts - Промпттар\n\n"
        "⚡ <b>Модельдер:</b>\n"
        "/benchmark - Жылдамдық тесті\n"
        "/tools - Function calling тесті\n"
        "/model pull - Модель жүктеу\n\n"
        "📅 <b>Басқа:</b>\n"
        "/calendar - Google Calendar\n\n"
        "💬 Кез келген сұрақ жазыңыз 👇",
        parse_mode="HTML"
    )

@router.message(Command("ask"))
async def cmd_ask(message: types.Message):
    question = message.text.replace("/ask", "").strip()
    if not question:
        await message.answer("Использование: /ask <вопрос>")
        return
    sent = await message.answer("Ищу информацию...")
    from services.rag_service import ask_with_rag
    answer = await ask_with_rag(question)
    await sent.edit_text(answer)

@router.message(lambda m: m.text is not None)
async def chat_handler(message: types.Message):
    user_text = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    request_id = generate_request_id()

    with tracer.start_as_current_span("chat_handler") as span:
        span.set_attribute("user_id", user_id)
        span.set_attribute("request_id", request_id)

        log.info("message_received",
                 request_id=request_id,
                 user_id=user_id,
                 text=user_text)

        try:
            from utils.rate_limiter import check_rate_limit
            if not await check_rate_limit(user_id, chat_id):
                await message.answer("Слишком много запросов. Подождите минуту.")
                return

            sent = await message.answer("...")

            with tracer.start_as_current_span("model_call"):
                if await is_private_mode(user_id):
                    answer = ollama_chat([{"role": "user", "content": user_text}])
                    await sent.edit_text(f"🔒 {answer}")
                else:
                    answer = route_model(user_id, user_text)
                    await sent.edit_text(answer)

            span.set_attribute("response_length", len(answer))
            log.info("message_answered",
                     request_id=request_id,
                     response_length=len(answer))

        except Exception as e:
            span.record_exception(e)
            log.error("chat_error", request_id=request_id, error=str(e))
            await message.answer(f"❌ Қате: {str(e)}")