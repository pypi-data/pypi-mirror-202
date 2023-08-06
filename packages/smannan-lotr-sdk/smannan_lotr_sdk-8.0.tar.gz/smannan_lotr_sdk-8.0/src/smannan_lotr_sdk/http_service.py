import json
import logging
import os
import requests
import sys

BASE_URL = 'https://the-one-api.dev/v2'
API_ACCESS_KEY_NAME = 'LOTR_API_ACCESS_KEY'

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
