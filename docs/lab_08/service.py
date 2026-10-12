from models import Booking, BookingStatus, RoomStatus


class HotelBookingService:
    def __init__(self, repository, pricing_strategy):
        self.repository = repository
        self.pricing_strategy = pricing_strategy
        self.observers = []
        self.bookings: list[Booking] = []

    def attach(self, observer) -> None:
        self.observers.append(observer)

    def detach(self, observer) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, message: str) -> None:
        for observer in self.observers:
            observer.update(message)

    def change_strategy(self, pricing_strategy) -> None:
        self.pricing_strategy = pricing_strategy
        self.notify(f"Выбран тариф: {pricing_strategy.name}")

    def calculate_cost(self, room_id: int, nights: int) -> float:
        if nights <= 0:
            raise ValueError("Количество ночей должно быть положительным")
        room = self.repository.get(room_id)
        return self.pricing_strategy.calculate(room, nights)

    def book(self, room_id: int, nights: int) -> Booking:
        room = self.repository.get(room_id)
        if room.status != RoomStatus.FREE:
            raise ValueError("Номер уже забронирован")

        cost = self.calculate_cost(room_id, nights)
        room.status = RoomStatus.BOOKED
        self.repository.update(room)

        booking_id = len(self.bookings) + 1
        booking = Booking(
            booking_id,
            room_id,
            nights,
            cost,
            self.pricing_strategy.name,
        )
        self.bookings.append(booking)
        self.notify(
            f"Номер {room.number} забронирован на {nights} ноч. "
            f"Стоимость: {cost:.2f} руб."
        )
        return booking

    def get_booking(self, booking_id: int) -> Booking:
        for booking in self.bookings:
            if booking.id == booking_id:
                return booking
        raise ValueError("Бронирование не найдено")

    def cancel(self, booking_id: int) -> None:
        booking = self.get_booking(booking_id)
        if booking.status != BookingStatus.ACTIVE:
            raise ValueError("Бронирование уже отменено")

        room = self.repository.get(booking.room_id)
        room.status = RoomStatus.FREE
        self.repository.update(room)
        booking.status = BookingStatus.CANCELLED
        self.notify(f"Бронирование {booking.id} отменено. Номер {room.number} освобождён")

    def get_rooms(self):
        return self.repository.get_all()

    def get_bookings(self) -> list[Booking]:
        return list(self.bookings)
