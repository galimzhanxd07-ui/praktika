# mcp_servers/postgres_server.py
import asyncpg
import csv
import io
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("postgres")
DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Задача 9 — роли
ROLE_PERMISSIONS = {
    "student": ["query_users"],
    "teacher": ["query_users", "get_user_stats"],
    "admin":   ["query_users", "get_user_stats", "export_to_csv"],
}
current_role = "student"

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="query_users",
            description="Получить список пользователей",
            inputSchema={"type": "object", "properties": {
                "limit": {"type": "integer", "default": 10}
            }}
        ),
        Tool(
            name="get_user_stats",
            description="Статистика пользователей",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="export_to_csv",
            description="Экспорт пользователей в CSV",
            inputSchema={"type": "object", "properties": {}}
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # Проверка роли
    allowed = ROLE_PERMISSIONS.get(current_role, [])
    if name not in allowed:
        raise ValueError(
            f"Доступ запрещён: роль '{current_role}' не может вызывать '{name}'"
        )

    conn = await asyncpg.connect(DB_URL)
    try:
        if name == "query_users":
            limit = arguments.get("limit", 10)
            rows = await conn.fetch("SELECT id, username, created_at FROM users LIMIT $1", limit)
            result = "\n".join(f"{r['id']} | {r['username']} | {r['created_at']}" for r in rows)
            return [TextContent(type="text", text=result or "Нет данных")]

        elif name == "get_user_stats":
            row = await conn.fetchrow("SELECT COUNT(*) as total FROM users")
            return [TextContent(type="text", text=f"Всего пользователей: {row['total']}")]

        elif name == "export_to_csv":
            rows = await conn.fetch("SELECT id, username, created_at FROM users")
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["id", "username", "created_at"])
            for r in rows:
                writer.writerow([r["id"], r["username"], r["created_at"]])
            return [TextContent(type="text", text=output.getvalue())]

    finally:
        await conn.close()

    return [TextContent(type="text", text="Неизвестный инструмент")]

async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())