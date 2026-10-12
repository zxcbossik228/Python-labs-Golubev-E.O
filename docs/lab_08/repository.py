from typing import Protocol


class Repository(Protocol):
    def add(self, entity): ...
    def get(self, entity_id): ...
    def get_all(self): ...
    def update(self, entity): ...
    def delete(self, entity_id): ...


class InMemoryRepository:
    def __init__(self):
        self._items = {}

    def add(self, entity):
        if entity.id in self._items:
            raise ValueError("Объект с таким ID уже существует")
        self._items[entity.id] = entity

    def get(self, entity_id):
        if entity_id not in self._items:
            raise ValueError("Объект не найден")
        return self._items[entity_id]

    def get_all(self):
        return list(self._items.values())

    def update(self, entity):
        if entity.id not in self._items:
            raise ValueError("Объект не найден")
        self._items[entity.id] = entity

    def delete(self, entity_id):
        if entity_id not in self._items:
            raise ValueError("Объект не найден")
        del self._items[entity_id]
