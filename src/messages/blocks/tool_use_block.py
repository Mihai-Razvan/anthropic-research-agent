from typing import Any, Self
from anthropic.types.tool_use_block import ToolUseBlock as AnthropicToolUseBlock
from anthropic.types.tool_use_block_param import ToolUseBlockParam as AnthropicToolUseBlockParam
from .base_block import BaseBlock


class ToolUseBlock(BaseBlock[AnthropicToolUseBlock, AnthropicToolUseBlockParam]):
    tool_id: str
    name: str
    tool_input: dict[str, Any]

    def __init__(self, tool_id: str, name: str, tool_input: dict[str, Any]) -> None:
        super().__init__(block_type="tool_use")

        self.tool_id = tool_id
        self.name = name
        self.tool_input = tool_input

    @classmethod
    def from_anthropic_block(cls, block: AnthropicToolUseBlock) -> Self:
        new_block: ToolUseBlock = ToolUseBlock(
            tool_id=block.id,
            name=block.name,
            tool_input=block.input
        )

        return new_block

    def to_anthropic_block_param(self) -> AnthropicToolUseBlockParam:
        anthropic_block_param: AnthropicToolUseBlockParam = {
            "id": self.tool_id,
            "type": self.block_type,
            "name": self.name,
            "input": self.tool_input
        }

        return anthropic_block_param

