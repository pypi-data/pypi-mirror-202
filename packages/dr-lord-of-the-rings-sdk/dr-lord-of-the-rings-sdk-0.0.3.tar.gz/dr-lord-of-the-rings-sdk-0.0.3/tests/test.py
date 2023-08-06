import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lotr_sdk.movies import Movie
from lotr_sdk.quotes import Quote


class MovieQuoteTests(unittest.TestCase):

    def test_movies(self):
        # Test retrieving all movies
        movies = Movie.get()
        self.assertIsNotNone(movies)
        
    def test_movie_name_runtime_budget(self):
        # Test retrieving movie name, runtime, and budget
        movies = Movie.get()
        movie = movies[1]
        self.assertIsInstance(movie, dict)
        self.assertIn('name', movie)
        self.assertIn('runtimeInMinutes', movie)
        self.assertIn('budgetInMillions', movie)
        
    def test_quotes(self):
        # Test retrieving all quotes
        quotes = Quote.get()
        self.assertIsNotNone(quotes)
        
    def test_quote_dialog(self):
        # Test retrieving quote dialog
        quotes = Quote.get()
        quote_dialog_1 = quotes[1]['dialog']
        quote_dialog_43 = quotes[43]['dialog']
        self.assertIsInstance(quote_dialog_1, str)
        self.assertIsInstance(quote_dialog_43, str)
        
    def test_quote_id_dialog(self):
        # Test retrieving quote dialog by quote ID
        quote_id = Quote.get(id='5cd96e05de30eff6ebcce814')
        quote_dialog = quote_id.dialog
        self.assertIsInstance(quote_dialog, str)
        
    def test_movie_id_name(self):
        # Test retrieving movie name by movie ID
        movie_id = Movie.get(_id="5cd95395de30eff6ebccde5d")
        movie_name = movie_id.name
        self.assertEqual(movie_name, "The Return of the King")

        
    def test_movie_id_budget(self):
        # Test retrieving movie budget by movie ID
        movie_id = Movie.get(_id="5cd95395de30eff6ebccde5d")
        movie_budget = movie_id.budgetInMillions
        self.assertIsInstance(movie_budget, int)
        
    def test_movie_quotes(self):
        # Test retrieving quotes by movie ID
        movie_id = Movie.get(_id="5cd95395de30eff6ebccde5d")
        movie_quotes = Quote.get(movie=movie_id._id)
        self.assertIsNotNone(movie_quotes)
        
    def test_movie_quote_dialog(self):
        # Test retrieving quote dialog by movie ID
        movie_id = Movie.get(_id="5cd95395de30eff6ebccde5d")
        movie_quotes = Quote.get(movie=movie_id._id)
        quote_dialog = movie_quotes[3]['dialog']
        self.assertIsInstance(quote_dialog, str)
        
if __name__ == '__main__':
    unittest.main()