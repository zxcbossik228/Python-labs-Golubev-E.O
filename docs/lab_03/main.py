class Vehicle:
    def __init__(self, brand, model, speed=0):
        self.brand = brand
        self.model = model
        self.speed = speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if value < 0:
            raise ValueError("Скорость не может быть отрицательной")
        self._speed = value

    def accelerate(self, value):
        self.speed += value

    def stop(self):
        self.speed = 0

    def transport_indicator(self):
        return 0

    def get_info(self):
        return f"{self.brand} {self.model}, скорость: {self.speed} км/ч"

    def __str__(self):
        return self.get_info()


class Car(Vehicle):
    def __init__(self, brand, model, passengers, speed=0):
        super().__init__(brand, model, speed)
        self.passengers = passengers

    def transport_indicator(self):
        return self.passengers * self.speed

    def get_info(self):
        return super().get_info() + f", пассажиров: {self.passengers}"


class Truck(Vehicle):
    def __init__(self, brand, model, load_capacity, speed=0):
        super().__init__(brand, model, speed)
        self.load_capacity = load_capacity

    def transport_indicator(self):
        return self.load_capacity * self.speed

    def get_info(self):
        return super().get_info() + f", грузоподъёмность: {self.load_capacity} т"


class Fleet:
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def show_all(self):
        for vehicle in self.vehicles:
            print(vehicle.get_info())
            print("Транспортный показатель:", vehicle.transport_indicator())

    def total_indicator(self):
        total = 0
        for vehicle in self.vehicles:
            total += vehicle.transport_indicator()
        return total


def main():
    fleet = Fleet()

    car1 = Car("Toyota", "Camry", 5, 60)
    car2 = Car("Kia", "Rio", 5, 50)
    truck = Truck("KamAZ", "5490", 20, 40)

    fleet.add_vehicle(car1)
    fleet.add_vehicle(car2)
    fleet.add_vehicle(truck)

    print("=== АВТОПАРК ===")
    fleet.show_all()
    print("Общий транспортный показатель:", fleet.total_indicator())

    print("\nИзменение состояния автомобиля:")
    car1.accelerate(20)
    print(car1)
    car1.stop()
    print("После остановки:", car1)


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
