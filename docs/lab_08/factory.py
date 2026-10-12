from models import FamilyRoom, LuxuryRoom, StandardRoom


class RoomFactory:
    """Factory: создание разных типов гостиничных номеров."""

    @staticmethod
    def create(room_type: str, room_id: int, number: str, base_price: float):
        if base_price <= 0:
            raise ValueError("Цена номера должна быть положительной")

        creators = {
            "standard": StandardRoom,
            "luxury": LuxuryRoom,
            "family": FamilyRoom,
        }
        if room_type not in creators:
            raise ValueError("Неизвестный тип номера")

        return creators[room_type](room_id, number, base_price, room_type)
