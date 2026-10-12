from typing import Protocol
from models import Room


class ReadRepository(Protocol):
    def get(self, room_id: int) -> Room:
        ...

    def get_all(self) -> list[Room]:
        ...


class WriteRepository(Protocol):
    def add(self, room: Room) -> None:
        ...

    def update(self, room: Room) -> None:
        ...


class RoomRepository(ReadRepository, WriteRepository, Protocol):
    pass


class Notifier(Protocol):
    def send(self, message: str) -> None:
        ...


class PricingPolicy(Protocol):
    name: str

    def calculate(self, room: Room, nights: int) -> float:
        ...
