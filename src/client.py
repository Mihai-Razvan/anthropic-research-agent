from anthropic import Anthropic
from anthropic.types import Message as AnthropicMessage, ToolParam
from anthropic.types.message_param import  MessageParam
from context.context_manager import ContextManager
from tools.tool_registry import ToolRegistry

class AnthropicClient:
    def __init__(
            self,
            model_name: str,
            max_tokens: int = 1024
    ) -> None:
        self.model_name = model_name
        self.max_tokens = max_tokens

        self.client: Anthropic = Anthropic()

    def call(self, ctx: ContextManager, tool_registry: ToolRegistry) -> AnthropicMessage:
        message_history: list[MessageParam] = [message.to_anthropic_message_param() for message in ctx.messages_history]
        tool_definitions: list[ToolParam] = [tool.to_anthropic_tool_param() for tool in tool_registry.available_tools]

        new_assistant_message: AnthropicMessage = self.client.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            messages=message_history,
            tools=tool_definitions
        )

        return new_assistant_message