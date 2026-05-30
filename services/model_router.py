from groq import Groq
from config.settings import GROQ_API_KEY
from services.memory import add_message, get_memory
from services.web_search import web_search

client = Groq(api_key=GROQ_API_KEY)


def route_model(user_id: int, text: str):

    # =========================
    # MEMORY SAVE (USER)
    # =========================
    add_message(user_id, "user", text)

    history = get_memory(user_id)

    # =========================
    # MODEL SELECT (SMART ROUTER)
    # =========================
    if len(text) < 50:
        model = "llama-3.1-8b-instant"
    else:
        model = "llama-3.3-70b-versatile"

    try:

        # =========================
        # AI REQUEST
        # =========================
        response = client.chat.completions.create(
            model=model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "Сен қазақ тілінде жауап беретін "
                        "ақылды AI көмекшісісің. "
                        "Әрқашан тек қазақ тілінде жауап бер."
                    )
                },
                *history
            ],

            temperature=0.7,
            max_tokens=1024
        )

        answer = response.choices[0].message.content

        # =========================
        # MEMORY SAVE (ASSISTANT)
        # =========================
        add_message(user_id, "assistant", answer)

        return answer

    except Exception as e:

        print("AI ERROR:", e)

        try:
            # =========================
            # WEB SEARCH FALLBACK
            # =========================
            result = web_search(text)

            if result:
                return result

            return "Интернеттен нәтиже табылмады."

        except Exception as web_error:

            print("WEB ERROR:", web_error)

            return "❌ Жүйе уақытша істемей тұр."

