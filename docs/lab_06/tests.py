import unittest
from models import BookingStatus, Guest, Room, RoomStatus
from services import HotelService


class HotelLab6Tests(unittest.TestCase):
    def setUp(self):
        self.service = HotelService()
        self.service.add_room(Room(1, "101", 1000))
        self.service.add_room(Room(2, "202", 2000))
        self.service.add_guest(Guest(1, "Иванов И.И.", "+70000000000"))

    def test_booking_and_cost(self):
        booking = self.service.book_room(1, 1, 3)
        self.assertEqual(self.service.calculate_cost(booking), 3000)
        self.assertEqual(self.service.get_room(1).status, RoomStatus.BOOKED)

    def test_check_in_and_out(self):
        booking = self.service.book_room(1, 1, 1)
        self.service.check_in(1)
        self.assertEqual(self.service.get_room(1).status, RoomStatus.OCCUPIED)
        self.service.check_out(1)
        self.assertEqual(self.service.get_room(1).status, RoomStatus.FREE)
        self.assertEqual(booking.status, BookingStatus.FINISHED)

    def test_cancel_booking(self):
        booking = self.service.book_room(1, 1, 1)
        self.service.cancel_booking(booking.id)
        self.assertEqual(booking.status, BookingStatus.CANCELLED)
        self.assertEqual(self.service.get_room(1).status, RoomStatus.FREE)

    def test_service_status(self):
        self.service.start_service(2)
        self.assertEqual(self.service.get_room(2).status, RoomStatus.SERVICE)
        self.service.finish_service(2)
        self.assertEqual(self.service.get_room(2).status, RoomStatus.FREE)

    def test_invalid_nights(self):
        with self.assertRaises(ValueError):
            self.service.book_room(1, 1, 0)


if __name__ == "__main__":
    unittest.main()
