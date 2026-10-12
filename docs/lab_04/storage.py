import csv
import json
from models import Movie


def save_json(movies, filename="movies.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump([movie.to_dict() for movie in movies], file, ensure_ascii=False, indent=4)


def load_json(filename="movies.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Movie.from_dict(item) for item in data]
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("Ошибка чтения JSON. Будет использован пустой каталог.")
        return []


def export_csv(movies, filename="movies.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "genre", "year", "rating"])
        for movie in movies:
            writer.writerow([movie.title, movie.genre, movie.year, movie.rating])
