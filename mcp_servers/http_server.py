# mcp_servers/http_server.py
import os
from aiohttp import web

SECRET_TOKEN = os.getenv("MCP_SECRET_TOKEN", "secret123")

async def handle(request):
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {SECRET_TOKEN}":
        return web.Response(status=401, text="Неверный токен")
    return web.Response(text="MCP сервер работает")

async def health(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get("/", handle)
app.router.add_get("/health", health)

if __name__ == "__main__":
    print("HTTP MCP сервер запущен на порту 8080")
    web.run_app(app, host="0.0.0.0", port=8080)