from dataclasses import dataclass
from enum import Enum


class RoomStatus(Enum):
    FREE = "свободен"
    BOOKED = "забронирован"
    OCCUPIED = "занят"
    SERVICE = "на обслуживании"


class BookingStatus(Enum):
    ACTIVE = "активно"
    FINISHED = "завершено"
    CANCELLED = "отменено"


@dataclass
class HotelEntity:
    id: int
    name: str

    def get_report_data(self) -> str:
        return f"{self.id}: {self.name}"


@dataclass
class Room(HotelEntity):
    price_per_night: float
    status: RoomStatus = RoomStatus.FREE

    def get_report_data(self) -> str:
        return (
            f"Номер {self.name} (ID {self.id}): {self.status.value}, "
            f"{self.price_per_night:.2f} руб./ночь"
        )


@dataclass
class Guest(HotelEntity):
    phone: str

    def get_report_data(self) -> str:
        return f"Гость {self.name} (ID {self.id}), телефон: {self.phone}"


@dataclass
class Booking(HotelEntity):
    room_id: int
    guest_id: int
    nights: int
    status: BookingStatus = BookingStatus.ACTIVE

    def get_report_data(self) -> str:
        return (
            f"Бронь {self.id}: номер ID {self.room_id}, гость ID {self.guest_id}, "
            f"ночей: {self.nights}, статус: {self.status.value}"
        )
