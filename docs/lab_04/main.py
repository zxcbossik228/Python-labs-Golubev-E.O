from exceptions import InvalidRatingError
from models import Movie
from services import MovieService
from storage import export_csv, load_json, save_json


def show(movies):
    if not movies:
        print("Фильмы не найдены")
        return
    for movie in movies:
        print(f"{movie.title} | {movie.genre} | {movie.year} | {movie.rating}")


def main():
    movies = load_json()
    service = MovieService(movies)

    while True:
        print("\n=== КАТАЛОГ ФИЛЬМОВ ===")
        print("1. Добавить")
        print("2. Показать все")
        print("3. Найти")
        print("4. Фильтр по рейтингу")
        print("5. Сортировка")
        print("6. Статистика")
        print("7. Сохранить JSON")
        print("8. Экспорт CSV")
        print("0. Выход")

        choice = input("Пункт: ")

        try:
            if choice == "1":
                movie = Movie(
                    input("Название: "),
                    input("Жанр: "),
                    int(input("Год: ")),
                    float(input("Рейтинг: ")),
                )
                service.add(movie)
            elif choice == "2":
                show(service.movies)
            elif choice == "3":
                show(service.search(input("Название или часть названия: ")))
            elif choice == "4":
                show(service.filter_by_rating(float(input("Минимальный рейтинг: "))))
            elif choice == "5":
                show(service.sort_by_rating())
            elif choice == "6":
                print(f"Средний рейтинг: {service.average_rating():.2f}")
            elif choice == "7":
                save_json(service.movies)
                print("Данные сохранены")
            elif choice == "8":
                export_csv(service.movies)
                print("CSV создан")
            elif choice == "0":
                save_json(service.movies)
                break
            else:
                print("Неизвестный пункт")
        except ValueError:
            print("Ошибка: введено число в неверном формате")
        except InvalidRatingError as error:
            print("Ошибка:", error)


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
