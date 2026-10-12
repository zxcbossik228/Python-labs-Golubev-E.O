from dataclasses import dataclass
from enum import Enum


class RoomStatus(Enum):
    FREE = "free"
    BOOKED = "booked"
    OCCUPIED = "occupied"


@dataclass
class Room:
    id: int
    number: str
    base_price: float
    status: RoomStatus = RoomStatus.FREE

    @property
    def room_type(self) -> str:
        return "room"


@dataclass
class StandardRoom(Room):
    @property
    def room_type(self) -> str:
        return "standard"


@dataclass
class LuxuryRoom(Room):
    @property
    def room_type(self) -> str:
        return "luxury"
