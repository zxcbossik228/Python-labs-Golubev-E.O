from context import OperationContext
from introspection import inspect_object
from models import Guest, Room
from protocols import print_report
from services import HotelService


def create_service() -> HotelService:
    service = HotelService()
    service.add_room(Room(1, "101", 2500))
    service.add_room(Room(2, "202", 4200))
    service.add_room(Room(3, "303", 5600))
    service.add_guest(Guest(1, "Голубев Е.О.", "+7-900-000-00-01"))
    return service


def show_rooms(service: HotelService) -> None:
    print("\n--- НОМЕРА ---")
    for room in service.rooms:
        print_report(room)


def show_guests(service: HotelService) -> None:
    print("\n--- ГОСТИ ---")
    if not service.guests:
        print("Гостей нет")
    for guest in service.guests:
        print_report(guest)


def show_bookings(service: HotelService) -> None:
    print("\n--- БРОНИРОВАНИЯ ---")
    if not service.bookings:
        print("Бронирований нет")
    for booking in service.bookings:
        print_report(booking)
        print(f"  Стоимость: {service.calculate_cost(booking):.2f} руб.")


def introspection_menu(service: HotelService) -> None:
    print("1. Номер")
    print("2. Гость")
    print("3. Бронирование")
    choice = input("Тип объекта: ")
    object_id = int(input("ID объекта: "))

    if choice == "1":
        obj = service.get_room(object_id)
    elif choice == "2":
        obj = service.get_guest(object_id)
    elif choice == "3":
        obj = service.get_booking(object_id)
    else:
        raise ValueError("Неизвестный тип объекта")

    inspect_object(obj)


def main() -> None:
    service = create_service()

    while True:
        print("\n=== ЛАБОРАТОРНАЯ №6. ГОСТИНИЦА ===")
        print("1. Показать номера")
        print("2. Показать гостей")
        print("3. Добавить гостя")
        print("4. Забронировать номер")
        print("5. Отменить бронирование")
        print("6. Заселить гостя")
        print("7. Выселить гостя")
        print("8. Поставить номер на обслуживание")
        print("9. Завершить обслуживание")
        print("10. Показать бронирования")
        print("11. Интроспекция объекта")
        print("12. Статистика")
        print("0. Выход")

        choice = input("Выберите пункт: ").strip()

        try:
            if choice == "1":
                show_rooms(service)
            elif choice == "2":
                show_guests(service)
            elif choice == "3":
                guest_id = int(input("ID гостя: "))
                name = input("ФИО гостя: ").strip()
                phone = input("Телефон: ").strip()
                service.add_guest(Guest(guest_id, name, phone))
                print("Гость добавлен")
            elif choice == "4":
                room_id = int(input("ID номера: "))
                guest_id = int(input("ID гостя: "))
                nights = int(input("Количество ночей: "))
                with OperationContext("Бронирование номера"):
                    booking = service.book_room(room_id, guest_id, nights)
                    print_report(booking)
                    print(f"Стоимость: {service.calculate_cost(booking):.2f} руб.")
            elif choice == "5":
                service.cancel_booking(int(input("ID бронирования: ")))
                print("Бронирование отменено")
            elif choice == "6":
                service.check_in(int(input("ID номера: ")))
                print("Заселение выполнено")
            elif choice == "7":
                service.check_out(int(input("ID номера: ")))
                print("Выселение выполнено")
            elif choice == "8":
                service.start_service(int(input("ID номера: ")))
                print("Номер переведён в статус 'на обслуживании'")
            elif choice == "9":
                service.finish_service(int(input("ID номера: ")))
                print("Обслуживание завершено")
            elif choice == "10":
                show_bookings(service)
            elif choice == "11":
                introspection_menu(service)
            elif choice == "12":
                print("\n--- СТАТИСТИКА ---")
                for key, value in service.statistics().items():
                    print(f"{key}: {value}")
            elif choice == "0":
                print("Работа программы завершена")
                break
            else:
                print("Неизвестный пункт меню")
        except (ValueError, RuntimeError) as error:
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
