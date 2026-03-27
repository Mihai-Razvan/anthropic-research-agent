from client import AnthropicClient
from messages import create_text_block_message_param


"""Loop Body"""
def loop_body(client: AnthropicClient) -> None:

    user_input: str = input("User: ")
    text_block_param = create_text_block_message_param(user_input)

    new_assistant_message = client.call(text_block_param)

    print(new_assistant_message.content)

"""Loop"""
def loop(client: AnthropicClient) -> None:

    while True:
        loop_body(client=client)