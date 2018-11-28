# Time keeping
from utils.timeit import timeit

class Article:
	# Variables shared by all instances

	def __init__(self, title, text, journal, link, date):
		# Variables specific to instance
		self.title = title
		self.text = text
		self.journal = journal
		self.link = link
		self.date = date

	def info(self):
		print(self.title)
		print(self.text)
		print(self.journal)
		print(self.link)
		print(self.date)

	def getArticle(self):
		return {
			'title' : self.title,
			'text' : self.text,
			'journal' : self.journal,
			'link' : self.link,
			'date' : self.date
		}
