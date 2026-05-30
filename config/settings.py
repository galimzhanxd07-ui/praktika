from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    GROQ_API_KEY: str
    groq_model_fast: str = "llama-3.1-8b-instant"
    groq_model_smart: str = "llama-3.3-70b-versatile"
    redis_url: str = "redis://localhost:6379"
    rate_limit_per_user: int = 10
    rate_limit_per_chat: int = 50
    context_max_tokens: int = 8000
    TAVILY_API_KEY: str = ""
    FERNET_KEY: str = ""

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()

BOT_TOKEN = settings.BOT_TOKEN
GROQ_API_KEY = settings.GROQ_API_KEY