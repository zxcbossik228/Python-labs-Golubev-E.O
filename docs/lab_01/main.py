def calculate_average(values):
    return sum(values) / len(values)


def longest_positive_period(values):
    current = 0
    maximum = 0

    for value in values:
        if value > 0:
            current += 1
            if current > maximum:
                maximum = current
        else:
            current = 0

    return maximum


def main():
    days = int(input("Введите количество дней: "))

    if days <= 0:
        print("Ошибка: количество дней должно быть больше нуля")
        return

    temperatures = []

    for i in range(days):
        temperature = float(input(f"Температура за день {i + 1}: "))
        temperatures.append(temperature)

    average = calculate_average(temperatures)
    maximum = max(temperatures)
    minimum = min(temperatures)

    positive_days = 0
    hot_days = 0

    for temperature in temperatures:
        if temperature > 0:
            positive_days += 1
        if temperature >= 30:
            hot_days += 1

    longest_period = longest_positive_period(temperatures)

    print("\nРезультаты анализа")
    print(f"Средняя температура: {average:.2f}")
    print(f"Максимальная температура: {maximum}")
    print(f"Минимальная температура: {minimum}")
    print(f"Дней выше нуля: {positive_days}")
    print(f"Жарких дней (30°C и выше): {hot_days}")
    print(f"Самый длинный положительный период: {longest_period} дней")


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
