from abc import ABC, abstractmethod
from typing import Literal, Generic, TypeVar, Self

AnthropicBlock = TypeVar("AnthropicBlock")
AnthropicBlockParam = TypeVar("AnthropicBlockParam")

class BaseBlock(ABC, Generic[AnthropicBlock, AnthropicBlockParam]):
    block_type: Literal["text", "tool_use"]

    def __init__(self, block_type: Literal["text", "tool_use"]) -> None:
        self.block_type = block_type

    @classmethod
    @abstractmethod
    def from_anthropic_block(cls, block: AnthropicBlock) -> Self:
        pass

    @abstractmethod
    def to_anthropic_block_param(self) -> AnthropicBlockParam:
        pass