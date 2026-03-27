from anthropic import Anthropic
from anthropic.types import Message
from anthropic.types.message_param import  MessageParam
from tools import available_tools

class AnthropicClient:
    def __init__(
            self,
            model_name: str,
            max_tokens: int = 1024
    ) -> None:
        self.model_name = model_name
        self.max_tokens = max_tokens

        self.client: Anthropic = Anthropic()
        self.message_history: list[MessageParam] = []

    def call(self, new_user_message: MessageParam) -> Message:
        self.message_history.append(new_user_message)

        new_assistant_message = self.client.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            messages=self.message_history,
            tools=[tool.to_anthropic_tool_param() for tool in available_tools]
        )

        return new_assistant_message