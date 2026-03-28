from .tool import Tool


class ToolRegistry:
    _available_tools: list[Tool]

    def __init__(self, tools: list[Tool]) -> None:
        self._available_tools = tools

    @property
    def available_tools(self) -> list[Tool]:
        return self._available_tools