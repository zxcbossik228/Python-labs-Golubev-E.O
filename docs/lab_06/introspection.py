import inspect
from models import HotelEntity


def inspect_object(obj) -> None:
    """Демонстрация механизмов интроспекции Python."""
    print("Тип объекта:", type(obj))
    print("Имя класса:", obj.__class__.__name__)
    print("Является HotelEntity:", isinstance(obj, HotelEntity))
    print("Есть атрибут id:", hasattr(obj, "id"))

    if hasattr(obj, "name"):
        print("Значение name через getattr():", getattr(obj, "name"))

    public_names = [name for name in dir(obj) if not name.startswith("_")]
    print("Публичные атрибуты из dir():", public_names)

    methods = [
        name
        for name, value in inspect.getmembers(obj, predicate=inspect.ismethod)
        if not name.startswith("_")
    ]
    print("Методы через inspect.getmembers():", methods)

    method = getattr(obj, "get_report_data", None)
    if method is not None:
        print("Сигнатура get_report_data():", inspect.signature(method))
