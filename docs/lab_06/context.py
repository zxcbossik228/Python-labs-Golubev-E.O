from datetime import datetime
import time


class OperationContext:
    """Собственный контекстный менеджер для журналирования операций."""

    def __init__(self, name: str, log_file: str = "operations.log"):
        self.name = name
        self.log_file = log_file
        self.start = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        print(f"[CONTEXT] Начало операции: {self.name}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        duration = time.perf_counter() - self.start
        result = "SUCCESS" if exc_type is None else "ERROR"

        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}]\n")
            file.write(f"Operation: {self.name}\n")
            file.write(f"Duration: {duration:.6f} sec\n")
            file.write(f"Result: {result}\n")
            if exc_type is not None:
                file.write(f"Exception: {exc_type.__name__}: {exc_value}\n")
            file.write("\n")

        if exc_type is None:
            print(f"[CONTEXT] Операция завершена успешно за {duration:.6f} sec")
        else:
            print(f"[CONTEXT] Ошибка {exc_type.__name__}: {exc_value}")

        # False означает, что исключение не скрывается.
        return False
