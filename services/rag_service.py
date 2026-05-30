# services/rag_service.py
import ollama
import json
import redis.asyncio as aioredis
from groq import AsyncGroq
from config.settings import settings

redis = aioredis.from_url(settings.redis_url, decode_responses=True)
groq = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def get_embedding(text: str) -> list[float]:
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]

def cosine_similarity(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x ** 2 for x in a) ** 0.5
    nb = sum(x ** 2 for x in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0

async def add_document(doc_id: str, text: str):
    embedding = await get_embedding(text)
    await redis.set(f"doc:{doc_id}", json.dumps({
        "text": text,
        "embedding": embedding
    }))

async def search_documents(query: str, top_k: int = 5) -> list[str]:
    query_emb = await get_embedding(query)
    keys = await redis.keys("doc:*")

    scores = []
    for key in keys:
        raw = await redis.get(key)
        doc = json.loads(raw)
        score = cosine_similarity(query_emb, doc["embedding"])
        scores.append((score, doc["text"]))

    scores.sort(reverse=True)
    return [text for _, text in scores[:top_k]]

async def ask_with_rag(question: str) -> str:
    docs = await search_documents(question)
    context = "\n\n".join(docs)

    response = await groq.chat.completions.create(
        model=settings.groq_model_fast,
        messages=[
            {"role": "system", "content": f"Используй этот контекст для ответа:\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content