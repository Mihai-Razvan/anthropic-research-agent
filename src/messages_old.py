from anthropic.types.text_block_param import TextBlockParam
from anthropic.types.message_param import MessageParam
from typing import Union

def create_text_block_message_param(text: str) -> MessageParam:
    text_block_param: TextBlockParam = {
        "type": "text",
        "text": text
    }

    return _build_message(text_block_param)

ContentBlock = Union[TextBlockParam]

def _build_message(block_param: ContentBlock) -> MessageParam:
    message_param: MessageParam = {
        "role": "user",
        "content": [
            block_param
        ]
    }

    return message_param