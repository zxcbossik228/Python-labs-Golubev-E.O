import time
from functools import wraps


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] вызван метод {func.__name__}()")
        result = func(*args, **kwargs)
        print(f"[LOG] метод {func.__name__}() завершён")
        return result

    return wrapper


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"[PERFORMANCE] {func.__name__}: {duration:.6f} sec")
        return result

    return wrapper


def limit_calls(max_calls):
    """Декоратор с параметром: ограничивает число вызовов функции."""

    def decorator(func):
        calls = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls
            if calls >= max_calls:
                raise RuntimeError("Превышено допустимое число вызовов операции")
            calls += 1
            return func(*args, **kwargs)

        return wrapper

    return decorator
