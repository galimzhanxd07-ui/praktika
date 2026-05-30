# services/search_service.py
import redis.asyncio as aioredis
from tavily import TavilyClient
from config.settings import settings

redis = aioredis.from_url(settings.redis_url, decode_responses=True)
tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)

async def search_web(query: str) -> str:
    # Проверяем кэш
    cache_key = f"search:{query}"
    cached = await redis.get(cache_key)
    if cached:
        return cached

    # Поиск
    results = tavily.search(query=query, max_results=5)
    formatted = ""
    for r in results["results"]:
        formatted += f"📌 {r['title']}\n{r['url']}\n{r['content'][:200]}...\n\n"

    # Кэшируем на 1 час
    await redis.set(cache_key, formatted, ex=3600)
    return formatted