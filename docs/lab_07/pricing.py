class StandardPricing:
    name = "Обычный тариф"

    def calculate(self, room, nights: int) -> float:
        return room.base_price * nights


class WeekendPricing:
    name = "Тариф выходного дня"

    def calculate(self, room, nights: int) -> float:
        return room.base_price * nights * 1.20


class SeasonalPricing:
    name = "Сезонный тариф"

    def calculate(self, room, nights: int) -> float:
        return room.base_price * nights * 1.30
