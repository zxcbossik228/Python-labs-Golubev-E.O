def films_by_year(films, year):
    for film in films:
        if film.year == year:
            yield film


class FilmIterator:
    def __init__(self, films):
        self.films = films
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.films):
            raise StopIteration
        film = self.films[self.index]
        self.index += 1
        return film
