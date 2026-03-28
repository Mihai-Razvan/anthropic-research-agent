from client import AnthropicClient
from messages.message import Message

from anthropic.types.text_block import TextBlock as AnthropicTextBlock
from anthropic.types.tool_use_block import ToolUseBlock as AnthropicToolUseBlock
from anthropic.types import Message as AnthropicMessage

from messages.blocks.text_block import TextBlock
from messages.blocks.tool_use_block import ToolUseBlock
from context.context_manager import ContextManager

def convert_response_to_message(response_message: AnthropicMessage) -> Message:
    message: Message = Message(role="assistant")

    for anthropic_block in response_message.content:
        new_block = None

        if isinstance(anthropic_block, AnthropicTextBlock):
            new_block = TextBlock.from_anthropic_block(block=anthropic_block)
        elif isinstance(anthropic_block, AnthropicToolUseBlock):
            new_block = ToolUseBlock.from_anthropic_block(block=anthropic_block)

        message.add_content_block(new_block)

    return message


"""Loop Body"""
def loop_body(client: AnthropicClient, ctx: ContextManager) -> None:

    user_input: str = input("## User: ")

    # Build message based on user input
    text_block_param: TextBlock = TextBlock(text=user_input)
    new_user_message = Message(role="user")
    new_user_message.add_content_block(text_block_param)

    # Add new user message to context message history
    ctx.messages_history.append(new_user_message)

    # Send a message to the anthropic client
    response_message: AnthropicMessage = client.call(ctx)

    # Convert the received response message from anthropic and add to context message history
    new_message: Message = convert_response_to_message(response_message)
    ctx.add_message_to_history(new_message)

    for content_block in response_message.content:
        print("Assistant: ", content_block)

"""Loop"""
def loop(client: AnthropicClient, ctx: ContextManager) -> None:

    while True:
        loop_body(client=client, ctx=ctx)