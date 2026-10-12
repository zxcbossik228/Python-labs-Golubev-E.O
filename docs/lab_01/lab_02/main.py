def add_movie(movies):
    title = input("Название: ")
    genre = input("Жанр: ")
    year = int(input("Год: "))
    rating = float(input("Рейтинг: "))

    movie = {
        "title": title,
        "genre": genre,
        "year": year,
        "rating": rating,
    }
    movies.append(movie)


def show_movies(movies):
    if not movies:
        print("Список фильмов пуст")
        return

    for movie in movies:
        print(movie["title"], "|", movie["genre"], "|", movie["year"], "|", movie["rating"])


def search_by_genre(movies, genre):
    result = []
    for movie in movies:
        if movie["genre"].lower() == genre.lower():
            result.append(movie)
    return result


def filter_by_rating(movies, minimum):
    result = []
    for movie in movies:
        if movie["rating"] >= minimum:
            result.append(movie)
    return result


def statistics(movies):
    if not movies:
        return 0, None, None

    average = sum(movie["rating"] for movie in movies) / len(movies)
    best = max(movies, key=lambda movie: movie["rating"])
    worst = min(movies, key=lambda movie: movie["rating"])
    return average, best, worst


def main():
    movies = [
        {"title": "Интерстеллар", "genre": "Фантастика", "year": 2014, "rating": 8.7},
        {"title": "Дюна", "genre": "Фантастика", "year": 2021, "rating": 8.0},
        {"title": "1+1", "genre": "Комедия", "year": 2011, "rating": 8.8},
        {"title": "Джокер", "genre": "Драма", "year": 2019, "rating": 8.4},
        {"title": "Начало", "genre": "Фантастика", "year": 2010, "rating": 8.7},
    ]

    while True:
        print("\n=== ФИЛЬМЫ ===")
        print("1. Добавить фильм")
        print("2. Показать все фильмы")
        print("3. Поиск по жанру")
        print("4. Фильтр по рейтингу")
        print("5. Сортировка по рейтингу")
        print("6. Статистика")
        print("7. Уникальные жанры")
        print("0. Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            add_movie(movies)
        elif choice == "2":
            show_movies(movies)
        elif choice == "3":
            genre = input("Введите жанр: ")
            show_movies(search_by_genre(movies, genre))
        elif choice == "4":
            minimum = float(input("Минимальный рейтинг: "))
            show_movies(filter_by_rating(movies, minimum))
        elif choice == "5":
            sorted_movies = sorted(movies, key=lambda movie: movie["rating"], reverse=True)
            show_movies(sorted_movies)
        elif choice == "6":
            average, best, worst = statistics(movies)
            print(f"Средний рейтинг: {average:.2f}")
            print("Лучший фильм:", best["title"])
            print("Фильм с минимальным рейтингом:", worst["title"])
        elif choice == "7":
            genres = {movie["genre"] for movie in movies}
            print("Уникальные жанры:", ", ".join(sorted(genres)))
        elif choice == "0":
            break
        else:
            print("Неизвестный пункт меню")


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
