from abc import ABC, abstractmethod


class TariffStrategy(ABC):
    name = "Тариф"

    @abstractmethod
    def calculate(self, room, nights: int) -> float:
        pass


class StandardTariff(TariffStrategy):
    name = "Обычный тариф"

    def calculate(self, room, nights: int) -> float:
        return room.base_price * nights


class SeasonalTariff(TariffStrategy):
    name = "Сезонный тариф"

    def calculate(self, room, nights: int) -> float:
        return room.base_price * nights * 1.30


class WeekendTariff(TariffStrategy):
    name = "Тариф выходного дня"

    def calculate(self, room, nights: int) -> float:
        return room.base_price * nights * 1.20
