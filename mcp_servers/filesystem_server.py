# mcp_servers/filesystem_server.py
import os
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource, Prompt, PromptMessage

ALLOWED_DIR = "./allowed_files"
os.makedirs(ALLOWED_DIR, exist_ok=True)

server = Server("filesystem")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_files",
            description="Показать файлы в разрешённой директории",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": "."}
                }
            }
        ),
        Tool(
            name="read_file",
            description="Прочитать содержимое файла",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string"}
                },
                "required": ["filename"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "list_files":
        files = os.listdir(ALLOWED_DIR)
        return [TextContent(type="text", text="\n".join(files) or "Папка пуста")]
    elif name == "read_file":
        filepath = os.path.join(ALLOWED_DIR, arguments["filename"])
        if not os.path.exists(filepath):
            return [TextContent(type="text", text="Файл не найден")]
        with open(filepath, "r", encoding="utf-8") as f:
            return [TextContent(type="text", text=f.read())]
    return [TextContent(type="text", text="Неизвестный инструмент")]

@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="file://templates/report",
            name="Шаблон отчёта",
            description="Стандартный шаблон для отчётов",
            mimeType="text/plain"
        ),
        Resource(
            uri="file://templates/letter",
            name="Шаблон письма",
            description="Шаблон делового письма",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri == "file://templates/report":
        return "# Отчёт\n\n**Дата:**\n**Автор:**\n**Содержание:**\n"
    elif uri == "file://templates/letter":
        return "Уважаемый...\n\nС уважением,\n"
    raise ValueError(f"Ресурс не найден: {uri}")

@server.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="summarize",
            description="Суммаризация текста",
        ),
        Prompt(
            name="translate_kz",
            description="Перевод на казахский язык",
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    if name == "summarize":
        return [PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text="Кратко суммаризируй следующий текст:"
            )
        )]
    elif name == "translate_kz":
        return [PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text="Переведи на казахский язык:"
            )
        )]

async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())