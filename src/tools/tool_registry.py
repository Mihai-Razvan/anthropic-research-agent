from typing import Any
from .tool import Tool
from mcp_logic.mcp_client import MCPClient


class ToolRegistry:
    _available_tools: list[Tool]

    def __init__(self, tools: list[Tool]) -> None:
        self._available_tools = tools

    @property
    def available_tools(self) -> list[Tool]:
        return self._available_tools

    async def call_tool(self, mcp_client: MCPClient, name: str, tool_input: dict[str, Any]):
        tool: Tool = next(
            (t for t in self._available_tools if t.name == name),
            None
        )

        if tool is not None:
            return await tool.run(
                tool_name=name,
                mcp_client=mcp_client,
                **tool_input
            )

        raise ValueError(f"Tool '{name}' not found")