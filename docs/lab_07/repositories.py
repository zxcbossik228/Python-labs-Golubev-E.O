from models import Room


class InMemoryRoomRepository:
    """Хранилище отвечает только за сохранение объектов в памяти (SRP)."""

    def __init__(self):
        self._rooms: dict[int, Room] = {}

    def add(self, room: Room) -> None:
        if room.id in self._rooms:
            raise ValueError("Номер с таким ID уже существует")
        self._rooms[room.id] = room

    def get(self, room_id: int) -> Room:
        if room_id not in self._rooms:
            raise ValueError("Номер не найден")
        return self._rooms[room_id]

    def get_all(self) -> list[Room]:
        return list(self._rooms.values())

    def update(self, room: Room) -> None:
        if room.id not in self._rooms:
            raise ValueError("Номер не найден")
        self._rooms[room.id] = room
