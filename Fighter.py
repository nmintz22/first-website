class Fighter:
	def __init__(self, first_name, last_name, nickname):
		self.first_name = first_name
		self.last_name = last_name
		self.nickname = nickname

	def __repr__(self):
		return self.first_name.lower() + " " + self.last_name.lower()

	def __str__(self):
		return self.first_name + " \"" + self.nickname + "\" " + self.last_name