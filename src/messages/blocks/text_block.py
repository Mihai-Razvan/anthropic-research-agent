from typing import Self
from anthropic.types.text_block import TextBlock as AnthropicTextBlock
from anthropic.types.text_block_param import TextBlockParam as AnthropicTextBlockParam
from .base_block import BaseBlock


class TextBlock(BaseBlock[AnthropicTextBlock, AnthropicTextBlockParam]):
    text: str

    def __init__(self, text: str) -> None:
        super().__init__(block_type="text")

        self.text = text

    @classmethod
    def from_anthropic_block(cls, block: AnthropicTextBlock) -> Self:
        new_block: TextBlock = TextBlock(block.text)

        return new_block

    def to_anthropic_block_param(self) -> AnthropicTextBlockParam:
        anthropic_block_param: AnthropicTextBlockParam = {
            "type": self.block_type,
            "text": self.text
        }

        return anthropic_block_param
