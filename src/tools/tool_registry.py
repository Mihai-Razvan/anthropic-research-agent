from typing import Any
from .tool import Tool


class ToolRegistry:
    _available_tools: list[Tool]

    def __init__(self, tools: list[Tool]) -> None:
        self._available_tools = tools

    def call_tool(self, name: str, tool_input: dict[str, Any]) -> str:
        tool: Tool = [tool for tool in self._available_tools if tool.name == name][0]
        tool_call_response: Any = tool.run(**tool_input)

        return tool_call_response

    @property
    def available_tools(self) -> list[Tool]:
        return self._available_tools