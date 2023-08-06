from lotr_api_client import get_movies, get_movie_quotes

def test_get_all_movies():
	movies, status = get_movies()
	assert movies

	for movie in movies:
		assert movie.movie_id
		assert movie.movie_name

def test_unsuccessful_get_movies():
	movies, status = get_movies(movie_id='5')
	assert not movies

def test_get_one_movie():
	movie, status = get_movies(movie_id = '5cd95395de30eff6ebccde5d')
	assert movie and len(movie) == 1
	assert movie[0].movie_id == '5cd95395de30eff6ebccde5d'
	assert movie[0].movie_name == 'The Return of the King'

def test_get_movie_quotes():
	quotes, status = get_movie_quotes(movie_id = '5cd95395de30eff6ebccde5d', limit=1)
	assert quotes and len(quotes) == 1
	assert quotes[0].movie_id == '5cd95395de30eff6ebccde5d'

def test_unsuccessful_get_movie_quotes():
	quotes, status = get_movie_quotes(movie_id = '5', limit=1)
	assert not quotes