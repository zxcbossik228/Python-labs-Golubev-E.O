class MovieService:
    def __init__(self, movies):
        self.movies = movies

    def add(self, movie):
        self.movies.append(movie)

    def search(self, text):
        return [movie for movie in self.movies if text.lower() in movie.title.lower()]

    def filter_by_rating(self, minimum):
        return [movie for movie in self.movies if movie.rating >= minimum]

    def sort_by_rating(self):
        return sorted(self.movies, key=lambda movie: movie.rating, reverse=True)

    def average_rating(self):
        if not self.movies:
            return 0
        return sum(movie.rating for movie in self.movies) / len(self.movies)
