from dataclasses import dataclass
from exceptions import InvalidRatingError


@dataclass
class Movie:
    title: str
    genre: str
    year: int
    rating: float

    def __post_init__(self):
        if self.rating < 0 or self.rating > 10:
            raise InvalidRatingError("Рейтинг должен быть от 0 до 10")

    def to_dict(self):
        return {
            "title": self.title,
            "genre": self.genre,
            "year": self.year,
            "rating": self.rating,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["genre"],
            int(data["year"]),
            float(data["rating"]),
        )
