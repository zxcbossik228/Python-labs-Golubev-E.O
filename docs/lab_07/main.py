from models import LuxuryRoom, StandardRoom
from notifications import ConsoleNotifier
from pricing import StandardPricing
from repositories import InMemoryRoomRepository
from services import BookingService, ReportService, RoomService
from ui import ConsoleUI


def build_application() -> ConsoleUI:
    # Dependency Injection: зависимости создаются снаружи и передаются сервисам.
    repository = InMemoryRoomRepository()
    notifier = ConsoleNotifier()
    pricing = StandardPricing()

    room_service = RoomService(repository)
    booking_service = BookingService(repository, notifier, pricing)
    report_service = ReportService(repository)

    room_service.add_room(StandardRoom(1, "101", 2500))
    room_service.add_room(LuxuryRoom(2, "501", 6500))

    return ConsoleUI(room_service, booking_service, report_service)


def main() -> None:
    app = build_application()
    app.run()


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
