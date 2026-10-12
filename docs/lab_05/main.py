from generators import FilmIterator, films_by_year
from models import Movie, ShortMovie
from operations import (
    all_ratings_valid,
    average_duration,
    filter_objects,
    has_genre,
    sort_objects,
    transform_objects,
)


def main():
    films = [
        Movie("Интерстеллар", "Фантастика", 2014, 8.7, 169),
        Movie("Дюна", "Фантастика", 2021, 8.0, 155),
        Movie("1+1", "Комедия", 2011, 8.8, 112),
        ShortMovie("Короткий путь", "Драма", 2021, 7.2, 28),
    ]

    good = filter_objects(films, lambda movie: movie.rating >= 8)
    names = transform_objects(films, lambda movie: movie.title)
    sorted_films = sort_objects(films, lambda movie: movie.duration)

    print("Фильмы с рейтингом от 8:")
    for movie in good:
        print(movie.get_info())

    print("\nНазвания через map():", names)

    print("\nСортировка по продолжительности:")
    for movie in sorted_films:
        print(movie.get_info())

    print(f"\nСредняя продолжительность: {average_duration(films):.2f} мин.")
    print("Есть фантастика:", has_genre(films, "Фантастика"))
    print("Все рейтинги корректны:", all_ratings_valid(films))

    print("\nГенератор фильмов 2021 года:")
    for movie in films_by_year(films, 2021):
        print(movie.title)

    print("\nСобственный итератор:")
    for movie in FilmIterator(films):
        print(movie.title)


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
