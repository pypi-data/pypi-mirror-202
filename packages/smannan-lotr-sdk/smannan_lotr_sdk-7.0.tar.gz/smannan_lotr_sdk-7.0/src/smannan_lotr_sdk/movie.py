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