from models import LuxuryRoom, StandardRoom
from pricing import SeasonalPricing, StandardPricing, WeekendPricing


class ConsoleUI:
    """Только ввод/вывод. Бизнес-логики здесь нет (SRP)."""

    def __init__(self, room_service, booking_service, report_service):
        self.room_service = room_service
        self.booking_service = booking_service
        self.report_service = report_service

    def show_rooms(self) -> None:
        print("\n--- НОМЕРА ---")
        for room in self.room_service.get_all():
            print(
                f"ID={room.id}, №{room.number}, тип={room.room_type}, "
                f"цена={room.base_price:.2f}, статус={room.status.value}"
            )

    def choose_pricing(self) -> None:
        print("1. Обычный")
        print("2. Выходного дня")
        print("3. Сезонный")
        choice = input("Тариф: ").strip()

        strategies = {
            "1": StandardPricing(),
            "2": WeekendPricing(),
            "3": SeasonalPricing(),
        }
        if choice not in strategies:
            raise ValueError("Неизвестный тариф")

        self.booking_service.change_pricing(strategies[choice])
        print("Выбран:", self.booking_service.pricing.name)

    def add_room(self) -> None:
        room_id = int(input("ID номера: "))
        number = input("Номер комнаты: ").strip()
        price = float(input("Цена за ночь: "))
        print("1. Standard")
        print("2. Luxury")
        room_type = input("Тип: ").strip()

        if room_type == "1":
            room = StandardRoom(room_id, number, price)
        elif room_type == "2":
            room = LuxuryRoom(room_id, number, price)
        else:
            raise ValueError("Неизвестный тип номера")

        self.room_service.add_room(room)
        print("Номер добавлен")

    def run(self) -> None:
        while True:
            print("\n=== ЛАБОРАТОРНАЯ №7. SOLID — ГОСТИНИЦА ===")
            print("1. Показать номера")
            print("2. Добавить номер")
            print("3. Рассчитать стоимость")
            print("4. Забронировать")
            print("5. Заселить")
            print("6. Выселить")
            print("7. Сменить тариф")
            print("8. Отчёт")
            print("0. Выход")
            choice = input("Выберите пункт: ").strip()

            try:
                if choice == "1":
                    self.show_rooms()
                elif choice == "2":
                    self.add_room()
                elif choice == "3":
                    room_id = int(input("ID номера: "))
                    nights = int(input("Ночей: "))
                    cost = self.booking_service.calculate_cost(room_id, nights)
                    print(f"Стоимость: {cost:.2f} руб.")
                elif choice == "4":
                    room_id = int(input("ID номера: "))
                    nights = int(input("Ночей: "))
                    cost = self.booking_service.book(room_id, nights)
                    print(f"Бронирование создано. Стоимость: {cost:.2f} руб.")
                elif choice == "5":
                    self.booking_service.check_in(int(input("ID номера: ")))
                elif choice == "6":
                    self.booking_service.check_out(int(input("ID номера: ")))
                elif choice == "7":
                    self.choose_pricing()
                elif choice == "8":
                    report = self.report_service.build()
                    print("Всего:", report["total"])
                    print("Свободно:", report["free"])
                    print("Забронировано:", report["booked"])
                    print("Занято:", report["occupied"])
                elif choice == "0":
                    print("Работа программы завершена")
                    break
                else:
                    print("Неизвестный пункт меню")
            except ValueError as error:
                print("Ошибка:", error)
