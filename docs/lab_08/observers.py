from typing import Protocol


class Observer(Protocol):
    def update(self, message: str) -> None:
        ...


class ConsoleObserver:
    def update(self, message: str) -> None:
        print("[Observer]", message)


class HistoryObserver:
    def __init__(self):
        self.events: list[str] = []

    def update(self, message: str) -> None:
        self.events.append(message)
