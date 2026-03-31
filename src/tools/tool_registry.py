from typing import Any
from .tool import Tool, MCPTool
from mcp_logic.mcp_client import MCPClient


class ToolRegistry:
    _available_static_tools: list[Tool]
    _available_mcp_tools: list[MCPTool]

    def __init__(self, static_tools: list[Tool], mcp_tools: list[MCPTool]) -> None:
        self._available_static_tools = static_tools
        self._available_mcp_tools = mcp_tools

    def call_static_tool(self, name: str, tool_input: dict[str, Any]) -> str:
        tool = [tool for tool in self._available_static_tools if tool.name == name]
        if not tool:
            return "Static tool does not exist"

        tool = tool[0]
        tool_call_response: Any = tool.run(**tool_input)

        return tool_call_response

    async def call_mcp_tool(self, name: str, tool_input: dict[str, Any], mcp_client: MCPClient) -> str:
        tool: MCPTool = [tool for tool in self._available_mcp_tools if tool.name == name][0]
        tool_call_response: Any = await tool.run(tool_name=name, mcp_client=mcp_client, **tool_input)

        return tool_call_response

    @property
    def available_static_tools(self) -> list[Tool]:
        return self._available_static_tools

    @property
    def available_mcp_tools(self) -> list[MCPTool]:
        return self._available_mcp_tools