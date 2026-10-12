import unittest
from factory import RoomFactory
from models import BookingStatus, FamilyRoom, LuxuryRoom, RoomStatus, StandardRoom
from observers import HistoryObserver
from repository import InMemoryRepository
from service import HotelBookingService
from strategies import SeasonalTariff, StandardTariff, WeekendTariff


class PatternTests(unittest.TestCase):
    def test_factory_creates_all_room_types(self):
        self.assertIsInstance(RoomFactory.create("standard", 1, "101", 1000), StandardRoom)
        self.assertIsInstance(RoomFactory.create("luxury", 2, "501", 3000), LuxuryRoom)
        self.assertIsInstance(RoomFactory.create("family", 3, "303", 2000), FamilyRoom)

    def test_strategies(self):
        room = RoomFactory.create("standard", 1, "101", 1000)
        self.assertEqual(StandardTariff().calculate(room, 2), 2000)
        self.assertEqual(WeekendTariff().calculate(room, 2), 2400)
        self.assertEqual(SeasonalTariff().calculate(room, 2), 2600)

    def test_booking_changes_room_status(self):
        repo = InMemoryRepository()
        room = RoomFactory.create("standard", 1, "101", 1000)
        repo.add(room)
        service = HotelBookingService(repo, StandardTariff())
        booking = service.book(1, 2)
        self.assertEqual(booking.cost, 2000)
        self.assertEqual(room.status, RoomStatus.BOOKED)

    def test_observer_receives_event(self):
        repo = InMemoryRepository()
        repo.add(RoomFactory.create("standard", 1, "101", 1000))
        service = HotelBookingService(repo, StandardTariff())
        history = HistoryObserver()
        service.attach(history)
        service.book(1, 1)
        self.assertTrue(any("забронирован" in event for event in history.events))

    def test_busy_room_cannot_be_booked_twice(self):
        repo = InMemoryRepository()
        repo.add(RoomFactory.create("standard", 1, "101", 1000))
        service = HotelBookingService(repo, StandardTariff())
        service.book(1, 1)
        with self.assertRaises(ValueError):
            service.book(1, 1)

    def test_cancel_booking_frees_room(self):
        repo = InMemoryRepository()
        room = RoomFactory.create("standard", 1, "101", 1000)
        repo.add(room)
        service = HotelBookingService(repo, StandardTariff())
        booking = service.book(1, 1)
        service.cancel(booking.id)
        self.assertEqual(booking.status, BookingStatus.CANCELLED)
        self.assertEqual(room.status, RoomStatus.FREE)

    def test_strategy_can_be_changed(self):
        repo = InMemoryRepository()
        repo.add(RoomFactory.create("luxury", 2, "501", 3000))
        service = HotelBookingService(repo, StandardTariff())
        self.assertEqual(service.calculate_cost(2, 1), 3000)
        service.change_strategy(WeekendTariff())
        self.assertEqual(service.calculate_cost(2, 1), 3600)


if __name__ == "__main__":
    unittest.main()
