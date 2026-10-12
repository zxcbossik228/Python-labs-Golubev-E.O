class ConsoleNotifier:
    def send(self, message: str) -> None:
        print("[Уведомление]", message)


class CollectingNotifier:
    """Вторая реализация интерфейса Notifier, удобная для тестов."""

    def __init__(self):
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)
