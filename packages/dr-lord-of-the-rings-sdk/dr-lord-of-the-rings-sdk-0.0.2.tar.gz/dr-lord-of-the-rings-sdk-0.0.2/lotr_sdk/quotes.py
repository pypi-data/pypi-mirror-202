from lotr_sdk.api_methods import ApiMethods

class Quote(ApiMethods):
    """Class representing a quote from a Lord of the Rings movie"""

    def __init__(
        self, _id: str, dialog: str, movie: str, character: str, id: str
    ):
        """
        Initializes a Quote object with relevant attributes

        :param _id: quote's unique identifier
        :param dialog: the contents of the quote
        :param movie: identifier for the movie the quote is from
        :param character: identifier for which character says the quote
        :param id: redundant quote identifier
        """
        self._id = _id
        self.dialog = dialog
        self._movie = movie
        self._character = character
        self.id = id
        #self.name = dialog

    @property
    def movie(self):
        from .movies import Movie
        """Returns the movie associated with the quote"""
        movie = Movie.get(id=self._movie)
        if movie:
            return movie
        else:
            return None


    @staticmethod
    def _deserialize(json):
        """
        Deserializes a response into Quote objects and returns a list of Quote objects

        :param json: JSON response from API
        :return: List of Quote objects
        """
        results = []
        for item in json:
            quote = Quote(
                _id=item.get("_id"),
                dialog=item.get("dialog"),
                movie=item.get("movie"),
                character=item.get("character"),
                id=item.get("_id")
            )
            results.append(quote)
        return results
