def filter_objects(objects, predicate):
    return list(filter(predicate, objects))


def transform_objects(objects, operation):
    return list(map(operation, objects))


def sort_objects(objects, key_function):
    return sorted(objects, key=key_function)


def average_duration(objects):
    if not objects:
        return 0
    return sum(movie.duration for movie in objects) / len(objects)


def has_genre(objects, genre):
    return any(movie.genre.lower() == genre.lower() for movie in objects)


def all_ratings_valid(objects):
    return all(0 <= movie.rating <= 10 for movie in objects)
