# Lord of the Rings SDK

The Lord of the Rings SDK is a Python package that provides easy access to the Lord of the Rings API. It includes modules for interacting with the movies and quotes from the Lord of the Rings movies.

## Installation

To get started, you'll need to install the dr-lord-of-the-rings-sdk package.

```bash
pip install dr-lord-of-the-rings-sdk
```


## Importing the SDK

You can import the Lord of the Rings SDK in your Python project using the following import statement:

```python
from lotr_sdk.movies import Movie
from lotr_ssdk.quotes import Quote
```

This will allow you to use the Movie, and Quote classes from the SDK in your code.



## Usage

Here are some basic examples of how to use the Lord of the Rings SDK:

```python
from lotr_sdk.movies import Movie
from lotr_sdk.quotes import Quote


# Get the Quote object with the specified ID
quote_id = Quote.get(id='5cd96e05de30eff6ebcce814')
# Check if a Quote object was found and print its details
if quote_id:
    print("Dialog:", quote_id.dialog)
    print("Movie ID:", quote_id._movie)
    # Call the movie property to get the associated movie object
    movie = quote_id.movie
    if movie:
        print("Movie Title:", movie.name)
        print("Movie ID:", movie._id)
    else:
        print("Movie not found.")
else:
    print("Quote not found.")


# Get a Movie object with the specified ID
movie_id = Movie.get(_id='5cd95395de30eff6ebccde5d')
# Check if a Movie object was found
if movie_id:
    # Call the quotes property to get all quotes for the movie
    quotes = movie_id.quotes
    if quotes:
        for quote in quotes:
            print("Dialog:", quote['dialog'])
    else:
        print("No quotes found for Movie:", movie_id.name)
else:
    print("Movie not found.")


# Get all the movies
movies = Movie.get()
for movie in movies:
    print(movie['name'])
    print("Runtime in minutes: " + str(movie['runtimeInMinutes'])) 
    print("Budget in millions: " + str(movie['budgetInMillions'])) 
    print()

# Get specific movies
print(movies[1])
print()
print(movies[1]['name'])
print()

# Get all the quotes
quotes = Quote.get()
    for quote in quotes:
        print(quote)
print()

# Get specific quote
print(quotes[8])
print()
print(quotes[1]['dialog'])
print()

# Get a specific quote by id
quote_id = Quote.get(id='5cd96e05de30eff6ebcce814')  
print(quote_id.dialog)
print()

# Get information about a specific movie by id
movie_id = Movie.get(_id="5cd95395de30eff6ebccde5d")
print(movie_id.name)
print()

#Get specific quote from movie by movie id
movie_quote = Quote.get(movie=movie_id._id)
print(movie_quote[3]['dialog'])  

```

## Endpoints

The SDK interacts with the following endpoints:

- `/movies`: This endpoint returns a list of all the movies from the Lord of the Rings series.

- `/movies/<id>`: This endpoint returns information about a specific movie, identified by the id parameter.

- `/movie/<id>/quotes`: This endpoint returns a list of all the quotes from a specific movie, identified by the id parameter.

- `/movie/<id>/quotes/<id>`: This endpoint returns a specific quote from a specific movie, identified by the id parameter.

- `/quotes`: This endpoint returns a list of all the quotes from the Lord of the Rings movies.

- `/quotes/<id>`: This endpoint returns information about a specific quote, identified by the id parameter.

