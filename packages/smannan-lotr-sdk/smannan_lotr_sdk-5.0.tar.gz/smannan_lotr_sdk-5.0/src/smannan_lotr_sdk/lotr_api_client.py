from http_service import get_request
from movie import Movie
from quote import Quote

"""
Get all movies or optionally one movie specified by movie_id

@param movie_id: the id of the movie to retrieve from the API
@param limit: the maximum number of results to return
@param page: the current page of results
@param offset: the offset into the page

@return: list of movies if successful else empty list and error
"""
def get_movies(movie_id: str = None, limit: int = None, page: int = None, offset: int = None):
	# get all movies by default or a specific movie if the user specifies
	relative_path = '/movie'
	if movie_id:
		relative_path = '/movie/{0}'.format(movie_id)

	# optional query parameters for pagination
	params = {
		'limit': limit,
		'page': page,
		'offset': offset
	}
	response, status = http_service.get_request(relative_path, params=params)

	# return an empty list of movies if the API call is unsuccessful
	if status != 200:
		return [], response['message']

	# parse movies from API response
	movies = []
	for document in response['docs']:
		movies.append(Movie(document))

	# return movie list and nil error on success
	return movies, None

"""
Get all quotes for a movie

@param movie_id: the id of the movie to retrieve quotes for
@param limit: the maximum number of results to return
@param page: the current page of results
@param offset: the offset into the page

@return list of quotes if successful or empty list and error
"""
def get_movie_quotes(movie_id: str, limit: int = None, page: int = None, offset: int = None):
	# get quotes for a specific movie
	relative_path = '/movie/{0}/quote'.format(movie_id)

	# optional query parameters for pagination
	params = {
		'limit': limit,
		'page': page,
		'offset': offset
	}

	response, status = http_service.get_request(relative_path, params=params)

	# return an empty list of movies if the API call is unsuccessful
	if status != 200:
		return [], response['message']

	# parse movies from API response
	quotes = []
	for document in response['docs']:
		quotes.append(Quote(document))

	# return movie list and nil error on success
	return quotes, None
