from dataclasses import dataclass
from enum import Enum


class RoomStatus(Enum):
    FREE = "free"
    BOOKED = "booked"


class BookingStatus(Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


@dataclass
class Room:
    id: int
    number: str
    base_price: float
    room_type: str
    status: RoomStatus = RoomStatus.FREE


@dataclass
class StandardRoom(Room):
    pass


@dataclass
class LuxuryRoom(Room):
    pass


@dataclass
class FamilyRoom(Room):
    pass


@dataclass
class Booking:
    id: int
    room_id: int
    nights: int
    cost: float
    tariff: str
    status: BookingStatus = BookingStatus.ACTIVE
