from typing import Any, Self
from dataclasses import dataclass
from anthropic.types.tool_result_block_param import ToolResultBlockParam as AnthropicToolResultBlockParam
from .base_block import BaseBlock


@dataclass
class ToolResultBlock(BaseBlock[Any, AnthropicToolResultBlockParam]):
    tool_use_id: str
    content: str

    def __init__(self, tool_use_id: str, content: str) -> None:
        super().__init__(block_type="tool_result")

        self.tool_use_id = tool_use_id
        self.content= content

    @classmethod
    def from_anthropic_block(cls, block: Any) -> Self:
        new_block: Any = Any()

        return new_block

    def to_anthropic_block_param(self) -> AnthropicToolResultBlockParam:
        anthropic_block_param: AnthropicToolResultBlockParam = {
            "tool_use_id": self.tool_use_id,
            "type": self.block_type,
            "content": self.content
        }

        return anthropic_block_param

