import json
import logging
import os
import requests
import sys

BASE_URL = 'https://the-one-api.dev/v2'
API_ACCESS_KEY_NAME = 'LOTR_API_ACCESS_KEY'

class Quote:
	def __init__(self, document):
		self.quote_id = document['_id']
		self.movie_id = document['movie']
		self.character_id = document['character']
		self.quote = document['dialog']

	def __str__(self):
		return self.quote

	def __repr__(self):
		return self.quote

class Movie:
	def __init__(self, document):
		self.movie_id = document['_id']
		self.movie_name = document['name']
		self.runtime_in_minutes = document['runtimeInMinutes']
		self.budget_in_millions = document['budgetInMillions']
		self.box_office_revenue_in_millions = document['boxOfficeRevenueInMillions']
		self.academy_award_nominations = document['academyAwardNominations']
		self.academy_award_wins = document['academyAwardWins']
		self.rotten_tomatoes_score = document['rottenTomatoesScore']

	def __str__(self):
		return self.movie_name

	def __repr__(self):
		return self.movie_name

"""
@param path: the relative path to the resource
@param params: dictionary with optional query parameters

@return (status, response_json): http status code and response json from get request
"""
def get_request(path: str, params={}) -> tuple:
	# get API access key from environment if available
	access_key = ''
	if API_ACCESS_KEY_NAME in os.environ:
		access_key = os.environ[API_ACCESS_KEY_NAME]
	else:
		logging.warning("Access key not found. Set environment variable: export LOTR_API_ACCESS_KEY=<your-api-key>")

	# make get request
	headers = {"Authorization": "Bearer {0}".format(access_key)}
	response = requests.get("{0}/{1}".format(BASE_URL, path), headers=headers, params=params)

	# return status code and json
	return json.loads(response.text), response.status_code

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
