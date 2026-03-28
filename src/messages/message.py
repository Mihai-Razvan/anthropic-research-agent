from typing import Literal, Union
from .blocks.text_block import TextBlock
from .blocks.tool_use_block import ToolUseBlock
from anthropic.types.message_param import MessageParam


class Message:
    role: Literal["user", "assistant"]
    content: list[
        Union[
            TextBlock,
            ToolUseBlock
        ]
    ]

    def __init__(self, role: Literal["user", "assistant"]) -> None:
        self.role = role
        self.content = []

    def add_content_block(
            self,
            content_block: Union[
                TextBlock,
                ToolUseBlock
            ]
    ) -> None:
        self.content.append(content_block)

    def to_anthropic_message_param(self) -> MessageParam:
        message_param: MessageParam = {
            "role": self.role,
            "content": [block.to_anthropic_block_param() for block in self.content]
        }

        return message_param
