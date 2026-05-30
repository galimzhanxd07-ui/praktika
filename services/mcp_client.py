# services/mcp_client.py
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPAggregator:
    def __init__(self):
        self.servers = {
            "fs":  StdioServerParameters(command="python", args=["mcp_servers/filesystem_server.py"]),
            "pg":  StdioServerParameters(command="python", args=["mcp_servers/postgres_server.py"]),
        }
        self.sessions: dict = {}
        self.tools: dict = {}  # {"fs__list_files": ("fs", "list_files"), ...}

    async def connect_all(self):
        for prefix, params in self.servers.items():
            try:
                read, write = await stdio_client(params).__aenter__()
                session = ClientSession(read, write)
                await session.__aenter__()
                await session.initialize()
                self.sessions[prefix] = session

                # Собираем инструменты с префиксами
                tools = await session.list_tools()
                for tool in tools.tools:
                    self.tools[f"{prefix}__{tool.name}"] = (prefix, tool.name)

                print(f"MCP сервер '{prefix}' подключён")
            except Exception as e:
                print(f"Не удалось подключить '{prefix}': {e}")

    async def call_tool(self, full_name: str, arguments: dict) -> str:
        if full_name not in self.tools:
            return f"Инструмент '{full_name}' не найден"

        prefix, tool_name = self.tools[full_name]
        session = self.sessions.get(prefix)
        if not session:
            return f"Сервер '{prefix}' недоступен"

        result = await session.call_tool(tool_name, arguments)
        return result.content[0].text if result.content else "Нет ответа"

    def get_tools_list(self) -> list:
        return list(self.tools.keys())

# Глобальный экземпляр
aggregator = MCPAggregator()