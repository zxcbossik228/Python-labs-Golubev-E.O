from typing import Protocol


class Reportable(Protocol):
    def get_report_data(self) -> str:
        ...


def print_report(item: Reportable) -> None:
    print(item.get_report_data())
