import unittest
from models import LuxuryRoom, RoomStatus, StandardRoom
from notifications import CollectingNotifier
from pricing import SeasonalPricing, StandardPricing, WeekendPricing
from repositories import InMemoryRoomRepository
from services import BookingService, ReportService, RoomService


class HotelTests(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRoomRepository()
        self.room_service = RoomService(self.repo)
        self.room_service.add_room(StandardRoom(1, "101", 1000))
        self.room_service.add_room(LuxuryRoom(2, "501", 3000))
        self.notifier = CollectingNotifier()
        self.service = BookingService(self.repo, self.notifier, StandardPricing())

    def test_book_room(self):
        self.assertEqual(self.service.book(1, 2), 2000)
        self.assertEqual(self.repo.get(1).status, RoomStatus.BOOKED)

    def test_book_busy_room(self):
        self.service.book(1, 1)
        with self.assertRaises(ValueError):
            self.service.book(1, 1)

    def test_check_in_and_out(self):
        self.service.book(1, 1)
        self.service.check_in(1)
        self.assertEqual(self.repo.get(1).status, RoomStatus.OCCUPIED)
        self.service.check_out(1)
        self.assertEqual(self.repo.get(1).status, RoomStatus.FREE)

    def test_different_pricing_implementations(self):
        weekend = BookingService(self.repo, self.notifier, WeekendPricing())
        self.assertEqual(weekend.calculate_cost(2, 1), 3600)
        seasonal = BookingService(self.repo, self.notifier, SeasonalPricing())
        self.assertEqual(seasonal.calculate_cost(2, 1), 3900)

    def test_report(self):
        report = ReportService(self.repo).build()
        self.assertEqual(report["total"], 2)
        self.assertEqual(report["free"], 2)

    def test_notifier_is_injected(self):
        self.service.book(1, 1)
        self.assertEqual(len(self.notifier.messages), 1)


if __name__ == "__main__":
    unittest.main()
