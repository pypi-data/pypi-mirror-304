# sage_core/message.py

from typing import Any  # Добавляем импорт Any

class Message:
    """
    Класс, представляющий сообщение для передачи между отправителями и получателями.
    """
    HIGH_PRIORITY = 1
    MEDIUM_PRIORITY = 5
    LOW_PRIORITY = 10
    SHUTDOWN_PRIORITY = 0

    def __init__(self, sender: str, receiver: str, content: Any, priority: int = MEDIUM_PRIORITY):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority
