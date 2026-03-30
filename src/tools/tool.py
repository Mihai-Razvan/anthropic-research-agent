from dataclasses import dataclass
from typing import Any, Callable

from anthropic.types import ToolParam


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., str]

    def to_anthropic_tool_param(self) -> ToolParam:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "strict": True
        }

    def run(self, **kwargs) -> str:
        return self.handler(**kwargs)