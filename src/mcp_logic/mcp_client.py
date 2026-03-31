from contextlib import AsyncExitStack
from typing import Optional

from mcp import ClientSession, StdioServerParameters, stdio_client
from mcp import Tool as MCPTool


class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str) -> None:
        server_params = StdioServerParameters(
            command="python3",
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

    async def list_tools(self) -> list[MCPTool]:
        response = await self.session.list_tools()
        return response.tools

    async def call_tool(self, tool_name: str, **kwargs) -> str:
        response = await self.session.call_tool(name=tool_name, arguments=kwargs)
        return str(response.content)