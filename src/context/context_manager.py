from messages.message import Message

class ContextManager:

    def __init__(self) -> None:
        self._messages_history: list[Message] = []

    def add_message_to_history(self, new_message: Message) -> None:
        self._messages_history.append(new_message)

    @property
    def messages_history(self) -> list[Message]:
        return self._messages_history
