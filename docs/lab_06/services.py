from decorators import limit_calls, log_call, measure_time
from models import Booking, BookingStatus, Guest, Room, RoomStatus


class HotelService:
    def __init__(self):
        self.rooms: list[Room] = []
        self.guests: list[Guest] = []
        self.bookings: list[Booking] = []

    @log_call
    def add_room(self, room: Room) -> None:
        if any(item.id == room.id for item in self.rooms):
            raise ValueError("Номер с таким ID уже существует")
        if room.price_per_night <= 0:
            raise ValueError("Цена номера должна быть положительной")
        self.rooms.append(room)

    @log_call
    def add_guest(self, guest: Guest) -> None:
        if any(item.id == guest.id for item in self.guests):
            raise ValueError("Гость с таким ID уже существует")
        self.guests.append(guest)

    def get_room(self, room_id: int) -> Room:
        for room in self.rooms:
            if room.id == room_id:
                return room
        raise ValueError("Номер не найден")

    def get_guest(self, guest_id: int) -> Guest:
        for guest in self.guests:
            if guest.id == guest_id:
                return guest
        raise ValueError("Гость не найден")

    def get_booking(self, booking_id: int) -> Booking:
        for booking in self.bookings:
            if booking.id == booking_id:
                return booking
        raise ValueError("Бронирование не найдено")

    @log_call
    @measure_time
    @limit_calls(100)
    def book_room(self, room_id: int, guest_id: int, nights: int) -> Booking:
        room = self.get_room(room_id)
        self.get_guest(guest_id)

        if room.status != RoomStatus.FREE:
            raise ValueError("Номер недоступен для бронирования")
        if nights <= 0:
            raise ValueError("Количество ночей должно быть больше нуля")

        booking_id = len(self.bookings) + 1
        booking = Booking(
            booking_id,
            f"Бронь {booking_id}",
            room_id,
            guest_id,
            nights,
        )
        room.status = RoomStatus.BOOKED
        self.bookings.append(booking)
        return booking

    @log_call
    def cancel_booking(self, booking_id: int) -> None:
        booking = self.get_booking(booking_id)
        if booking.status != BookingStatus.ACTIVE:
            raise ValueError("Можно отменить только активное бронирование")

        room = self.get_room(booking.room_id)
        if room.status == RoomStatus.OCCUPIED:
            raise ValueError("Нельзя отменить бронирование после заселения")

        booking.status = BookingStatus.CANCELLED
        room.status = RoomStatus.FREE

    @log_call
    def check_in(self, room_id: int) -> None:
        room = self.get_room(room_id)
        if room.status != RoomStatus.BOOKED:
            raise ValueError("Номер должен быть забронирован")
        room.status = RoomStatus.OCCUPIED

    @log_call
    def check_out(self, room_id: int) -> None:
        room = self.get_room(room_id)
        if room.status != RoomStatus.OCCUPIED:
            raise ValueError("Выселить можно только из занятого номера")

        room.status = RoomStatus.FREE
        for booking in self.bookings:
            if booking.room_id == room_id and booking.status == BookingStatus.ACTIVE:
                booking.status = BookingStatus.FINISHED

    @log_call
    def start_service(self, room_id: int) -> None:
        room = self.get_room(room_id)
        if room.status != RoomStatus.FREE:
            raise ValueError("На обслуживание можно поставить только свободный номер")
        room.status = RoomStatus.SERVICE

    @log_call
    def finish_service(self, room_id: int) -> None:
        room = self.get_room(room_id)
        if room.status != RoomStatus.SERVICE:
            raise ValueError("Номер не находится на обслуживании")
        room.status = RoomStatus.FREE

    def calculate_cost(self, booking: Booking) -> float:
        room = self.get_room(booking.room_id)
        return room.price_per_night * booking.nights

    @measure_time
    def statistics(self) -> dict:
        return {
            "Всего номеров": len(self.rooms),
            "Свободно": sum(room.status == RoomStatus.FREE for room in self.rooms),
            "Забронировано": sum(room.status == RoomStatus.BOOKED for room in self.rooms),
            "Занято": sum(room.status == RoomStatus.OCCUPIED for room in self.rooms),
            "На обслуживании": sum(room.status == RoomStatus.SERVICE for room in self.rooms),
            "Гостей": len(self.guests),
            "Всего бронирований": len(self.bookings),
            "Активных броней": sum(
                booking.status == BookingStatus.ACTIVE for booking in self.bookings
            ),
        }
