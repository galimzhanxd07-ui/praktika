# services/image_service.py
import base64
from groq import AsyncGroq
from config.settings import settings

groq = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def analyze_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = await groq.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Опиши это изображение подробно на русском языке."
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content