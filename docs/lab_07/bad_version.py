"""
Намеренно проблемная версия лабораторной №7.
Она нужна для сравнения ДО и ПОСЛЕ рефакторинга по SOLID.
"""


class RoomBase:
    def book(self):
        return "Номер забронирован"


class ServiceRoom(RoomBase):
    # LSP: наследник нельзя безопасно подставить вместо RoomBase.
    def book(self):
        raise RuntimeError("Служебный номер нельзя бронировать")


class BigHotelInterface:
    # ISP: один слишком большой интерфейс для несвязанных задач.
    def save_room(self): ...
    def book_room(self): ...
    def send_email(self): ...
    def build_report(self): ...


class HotelSystem:
    """Класс специально содержит сразу несколько архитектурных проблем."""

    def __init__(self):
        # DIP: бизнес-класс сам создаёт конкретное хранилище.
        self.rooms = {}

    def add_room(self, room_id, room_type, price):
        # SRP: этот же класс хранит данные, считает стоимость, уведомляет и печатает отчёт.
        self.rooms[room_id] = {"type": room_type, "price": price, "status": "free"}
        print("Номер добавлен")

    def book(self, room_id, nights, notify_type):
        room = self.rooms[room_id]
        if room["status"] != "free":
            raise ValueError("Номер занят")

        # OCP: при добавлении нового типа номера приходится менять существующий метод.
        if room["type"] == "standard":
            cost = room["price"] * nights
        elif room["type"] == "luxury":
            cost = room["price"] * nights * 1.5
        else:
            cost = room["price"] * nights * 1.2

        room["status"] = "booked"

        # OCP/DIP: способ уведомления жёстко закодирован условием.
        if notify_type == "console":
            print("Бронирование создано")
        elif notify_type == "email":
            print("Отправка email")

        print("Стоимость:", cost)
        return cost

    def report(self):
        print("Номеров:", len(self.rooms))
        print("Данные:", self.rooms)
