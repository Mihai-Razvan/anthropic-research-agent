from client import AnthropicClient
from context.context_manager import ContextManager
from tools.tool_registry import ToolRegistry
from messages.message import Message
from messages.blocks.text_block import TextBlock
from messages.blocks.tool_use_block import ToolUseBlock
from messages.blocks.tool_result_block import ToolResultBlock

from anthropic.types.text_block import TextBlock as AnthropicTextBlock
from anthropic.types.tool_use_block import ToolUseBlock as AnthropicToolUseBlock
from anthropic.types import Message as AnthropicMessage


def print_blocks(role: str, content_blocks) -> None:
    print()

    for content_block in content_blocks:
        print(f"{role}: ", content_block)


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

def make_user_call(client: AnthropicClient, ctx: ContextManager, tool_registry: ToolRegistry):
    response_message: AnthropicMessage | None = None

    while response_message is None or response_message.stop_reason == "tool_use":
        # Send a message to the anthropic client
        response_message = client.call(ctx, tool_registry)

        # Print response
        print_blocks(role="Assistant", content_blocks=response_message.content)

        # Convert the received response message from anthropic and add to context message history
        new_message: Message = convert_response_to_message(response_message)
        ctx.add_message_to_history(new_message)

        #
        tool_use_blocks = [block for block in new_message.content if isinstance(block, ToolUseBlock)]
        if not tool_use_blocks:
            continue

        new_tool_result_message = Message(role="user")
        for block in tool_use_blocks:
            # Make the corresponding tool call
            tool_response: str = tool_registry.call_tool(name=block.name, tool_input=block.tool_input)

            # Build the tool result block and add to the message
            tool_result_block: ToolResultBlock = ToolResultBlock(tool_use_id=block.tool_id, content=tool_response)
            new_tool_result_message.add_content_block(tool_result_block)

        # Add new user message to context message history
        ctx.messages_history.append(new_tool_result_message)
        print_blocks(role="(User) Tool Use Result", content_blocks=new_tool_result_message.content)


"""Loop Body"""
def loop_body(client: AnthropicClient, ctx: ContextManager, tool_registry: ToolRegistry) -> None:

    print("\n## Turn ##")
    user_input: str = input("User: ")

    # Build message based on user input
    text_block_param: TextBlock = TextBlock(text=user_input)
    new_user_message = Message(role="user")
    new_user_message.add_content_block(text_block_param)

    # Add new user message to context message history
    ctx.messages_history.append(new_user_message)

    make_user_call(client=client, ctx=ctx, tool_registry=tool_registry)

"""Loop"""
def loop(client: AnthropicClient, ctx: ContextManager, tool_registry: ToolRegistry) -> None:

    while True:
        loop_body(client=client, ctx=ctx, tool_registry=tool_registry)