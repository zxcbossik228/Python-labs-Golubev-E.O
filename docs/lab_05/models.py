class Film:
    def __init__(self, title, genre, year, rating, duration):
        self.title = title
        self.genre = genre
        self.year = year
        self.rating = rating
        self.duration = duration

    def get_info(self):
        return f"{self.title} ({self.year}), {self.genre}, {self.rating}, {self.duration} мин."


class Movie(Film):
    pass


class ShortMovie(Film):
    def get_info(self):
        return "Короткометражный: " + super().get_info()
