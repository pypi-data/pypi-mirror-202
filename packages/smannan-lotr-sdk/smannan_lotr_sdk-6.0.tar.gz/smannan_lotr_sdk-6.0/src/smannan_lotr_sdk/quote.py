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