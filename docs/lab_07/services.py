from interfaces import Notifier, PricingPolicy, ReadRepository, RoomRepository
from models import Room, RoomStatus


class RoomService:
    """Отдельная ответственность: управление списком номеров (SRP)."""

    def __init__(self, repository: RoomRepository):
        self.repository = repository

    def add_room(self, room: Room) -> None:
        if room.base_price <= 0:
            raise ValueError("Цена должна быть положительной")
        self.repository.add(room)

    def get_all(self) -> list[Room]:
        return self.repository.get_all()


class BookingService:
    """Бизнес-логика получает зависимости через конструктор (DIP + DI)."""

    def __init__(
        self,
        repository: RoomRepository,
        notifier: Notifier,
        pricing: PricingPolicy,
    ):
        self.repository = repository
        self.notifier = notifier
        self.pricing = pricing

    def change_pricing(self, pricing: PricingPolicy) -> None:
        self.pricing = pricing

    def calculate_cost(self, room_id: int, nights: int) -> float:
        if nights <= 0:
            raise ValueError("Количество ночей должно быть положительным")
        room = self.repository.get(room_id)
        return self.pricing.calculate(room, nights)

    def book(self, room_id: int, nights: int) -> float:
        room = self.repository.get(room_id)
        if room.status != RoomStatus.FREE:
            raise ValueError("Номер недоступен")

        cost = self.calculate_cost(room_id, nights)
        room.status = RoomStatus.BOOKED
        self.repository.update(room)
        self.notifier.send(
            f"Номер {room.number} забронирован. "
            f"Тариф: {self.pricing.name}. Стоимость: {cost:.2f} руб."
        )
        return cost

    def check_in(self, room_id: int) -> None:
        room = self.repository.get(room_id)
        if room.status != RoomStatus.BOOKED:
            raise ValueError("Сначала номер нужно забронировать")
        room.status = RoomStatus.OCCUPIED
        self.repository.update(room)
        self.notifier.send(f"Выполнено заселение в номер {room.number}")

    def check_out(self, room_id: int) -> None:
        room = self.repository.get(room_id)
        if room.status != RoomStatus.OCCUPIED:
            raise ValueError("Выселить можно только из занятого номера")
        room.status = RoomStatus.FREE
        self.repository.update(room)
        self.notifier.send(f"Номер {room.number} освобождён")


class ReportService:
    """Формирование отчётов вынесено из BookingService (SRP)."""

    def __init__(self, repository: ReadRepository):
        self.repository = repository

    def build(self) -> dict[str, int]:
        rooms = self.repository.get_all()
        return {
            "total": len(rooms),
            "free": sum(room.status == RoomStatus.FREE for room in rooms),
            "booked": sum(room.status == RoomStatus.BOOKED for room in rooms),
            "occupied": sum(room.status == RoomStatus.OCCUPIED for room in rooms),
        }
