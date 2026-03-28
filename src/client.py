from anthropic import Anthropic
from anthropic.types import Message as AnthropicMessage
from anthropic.types.message_param import  MessageParam
from tools import available_tools
from context.context_manager import ContextManager

class AnthropicClient:
    def __init__(
            self,
            model_name: str,
            max_tokens: int = 1024
    ) -> None:
        self.model_name = model_name
        self.max_tokens = max_tokens

        self.client: Anthropic = Anthropic()

    def call(self, ctx: ContextManager) -> AnthropicMessage:
        message_history: list[MessageParam] = [message.to_anthropic_message_param() for message in ctx.messages_history]

        new_assistant_message: AnthropicMessage = self.client.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            messages=message_history,
            tools=[tool.to_anthropic_tool_param() for tool in available_tools]
        )

        return new_assistant_message