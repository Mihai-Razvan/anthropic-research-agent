from dataclasses import dataclass
from typing import Any, Callable, Awaitable

from anthropic.types import ToolParam


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., Awaitable[str]]

    def to_anthropic_tool_param(self) -> ToolParam:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "strict": False
        }

    async def run(self, **kwargs) -> Any:
        return await self.handler(**kwargs)