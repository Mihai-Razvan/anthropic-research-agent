import time
import random
from typing import Optional
from anthropic import Anthropic
from anthropic.types import Message as AnthropicMessage, ToolParam
from anthropic.types.message_param import MessageParam
from context.context_manager import ContextManager
from tools.tool_registry import ToolRegistry

class AnthropicClient:
    def __init__(
            self,
            model_name: str,
            max_tokens: int = 1024,
            max_retries: int = 3,
            base_delay: float = 1.0,
            max_delay: float = 60.0
    ) -> None:
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

        self.client: Anthropic = Anthropic()

    def _exponential_backoff_delay(self, attempt: int) -> float:
        delay = min(self.base_delay * (2 ** attempt), self.max_delay)

        # Add some jitter to avoid thundering herd
        jitter = random.uniform(0.1, 0.3) * delay

        return delay + jitter

    def call(self, ctx: ContextManager, tool_registry: ToolRegistry) -> AnthropicMessage:
        message_history: list[MessageParam] = [message.to_anthropic_message_param() for message in ctx.messages_history]
        tool_definitions: list[ToolParam] = [
            tool.to_anthropic_tool_param()
            for tool in (
                    tool_registry.available_static_tools +
                    tool_registry.available_mcp_tools
            )
        ]

        last_exception: Optional[Exception] = None
        
        for attempt in range(self.max_retries + 1):
            try:
                new_assistant_message: AnthropicMessage = self.client.messages.create(
                    model=self.model_name,
                    max_tokens=self.max_tokens,
                    messages=message_history,
                    tools=tool_definitions
                )
                
                return new_assistant_message
            except Exception as e:
                last_exception = e
                print(f"Failed to call Anthropic: {str(e)}")
                
                # Don't retry if this was the last attempt
                if attempt == self.max_retries:
                    break
                
                # Calculate delay and wait before retrying
                delay = self._exponential_backoff_delay(attempt)
                time.sleep(delay)
        
        # If we get here, all retries failed
        raise last_exception