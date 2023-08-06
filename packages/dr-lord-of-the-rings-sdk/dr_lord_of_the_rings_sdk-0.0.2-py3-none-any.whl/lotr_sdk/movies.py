from lotr_sdk.api_methods import ApiMethods

class Movie(ApiMethods):
    """Class representing a Lord of the Rings movie"""

    def __init__(
        self,
        _id: str,
        name: str,
        runtimeInMinutes: int,
        budgetInMillions: float,
        boxOfficeRevenueInMillions: float,
        academyAwardNominations: int,
        academyAwardWins: int,
        rottenTomatoesScore: float,
    ):
        """
        Initializes a Movie object with relevant attributes

        :param _id: movie's unique identifier
        :param name: name of the movie
        :param runtime_in_minutes: runtime of the movie in minutes
        :param budget_in_millions: budget of the movie in millions
        :param box_office_revenue_in_millions: box office revenue of the movie in millions
        :param academy_award_nominations: number of academy award nominations for the movie
        :param academy_award_wins: number of academy award wins for the movie
        :param rotten_tomatoes_score: rotten tomatoes score for the movie
        """
        self._id = _id
        self.name = name
        self.runtimeInMinutes = runtimeInMinutes
        self.budgetInMillions = budgetInMillions
        self.boxOfficeRevenueInMillions = boxOfficeRevenueInMillions
        self.academyAwardNominations = academyAwardNominations
        self.academyAwardWins = academyAwardWins
        self.rottenTomatoesScore = rottenTomatoesScore

    @property
    def quotes(self):
        from .quotes import Quote
        """Returns a list of quotes associated with the movie"""
        quotes = Quote.get(movie=self._id)
        return quotes

    @staticmethod
    def _deserialize(data):
        """
        Deserializes a list of dictionaries into a list of objects.

        :param data: list of dictionaries
        :return: list of objects
        """
        movies = []
        for item in data:
            movie = Movie(
                _id=item["_id"],
                name=item["name"],
                runtimeInMinutes=item["runtimeInMinutes"],
                budgetInMillions=item["budgetInMillions"],
                boxOfficeRevenueInMillions=item["boxOfficeRevenueInMillions"],
                academyAwardNominations=item["academyAwardNominations"],
                academyAwardWins=item["academyAwardWins"],
                rottenTomatoesScore=item["rottenTomatoesScore"]
            )
            movies.append(movie)
        return movies
