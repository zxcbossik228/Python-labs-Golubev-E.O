from factory import RoomFactory
from observers import ConsoleObserver, HistoryObserver
from repository import InMemoryRepository
from service import HotelBookingService
from strategies import SeasonalTariff, StandardTariff, WeekendTariff


def create_application():
    repository = InMemoryRepository()
    repository.add(RoomFactory.create("standard", 1, "101", 2500))
    repository.add(RoomFactory.create("luxury", 2, "501", 7000))
    repository.add(RoomFactory.create("family", 3, "303", 4500))

    service = HotelBookingService(repository, StandardTariff())
    history = HistoryObserver()
    service.attach(ConsoleObserver())
    service.attach(history)
    return service, history


def show_rooms(service: HotelBookingService) -> None:
    print("\n--- НОМЕРА ---")
    for room in service.get_rooms():
        print(
            f"ID={room.id}, №{room.number}, тип={room.room_type}, "
            f"цена={room.base_price:.2f}, статус={room.status.value}"
        )


def show_bookings(service: HotelBookingService) -> None:
    print("\n--- БРОНИРОВАНИЯ ---")
    bookings = service.get_bookings()
    if not bookings:
        print("Бронирований нет")
    for booking in bookings:
        print(
            f"ID={booking.id}, room_id={booking.room_id}, ночей={booking.nights}, "
            f"стоимость={booking.cost:.2f}, тариф={booking.tariff}, "
            f"статус={booking.status.value}"
        )


def choose_tariff(service: HotelBookingService) -> None:
    print("1. Обычный тариф")
    print("2. Сезонный тариф")
    print("3. Тариф выходного дня")
    choice = input("Выберите тариф: ").strip()
    strategies = {
        "1": StandardTariff(),
        "2": SeasonalTariff(),
        "3": WeekendTariff(),
    }
    if choice not in strategies:
        raise ValueError("Неизвестный тариф")
    service.change_strategy(strategies[choice])


def main() -> None:
    service, history = create_application()

    while True:
        print("\n=== ЛАБОРАТОРНАЯ №8. ПАТТЕРНЫ — ГОСТИНИЦА ===")
        print("1. Показать номера")
        print("2. Рассчитать стоимость")
        print("3. Забронировать номер")
        print("4. Отменить бронирование")
        print("5. Сменить тариф (Strategy)")
        print("6. Показать бронирования")
        print("7. История уведомлений (Observer)")
        print("0. Выход")
        choice = input("Выберите пункт: ").strip()

        try:
            if choice == "1":
                show_rooms(service)
            elif choice == "2":
                room_id = int(input("ID номера: "))
                nights = int(input("Количество ночей: "))
                print(f"Стоимость: {service.calculate_cost(room_id, nights):.2f} руб.")
            elif choice == "3":
                room_id = int(input("ID номера: "))
                nights = int(input("Количество ночей: "))
                booking = service.book(room_id, nights)
                print(f"Создано бронирование ID {booking.id}")
            elif choice == "4":
                service.cancel(int(input("ID бронирования: ")))
            elif choice == "5":
                choose_tariff(service)
            elif choice == "6":
                show_bookings(service)
            elif choice == "7":
                if not history.events:
                    print("История пока пуста")
                for event in history.events:
                    print("-", event)
            elif choice == "0":
                print("Работа программы завершена")
                break
            else:
                print("Неизвестный пункт меню")
        except ValueError as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("\nОшибка программы:", error)
    finally:
        try:
            input("\nНажмите Enter, чтобы закрыть программу...")
        except EOFError:
            pass
