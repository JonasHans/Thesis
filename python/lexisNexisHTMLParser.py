from bs4 import BeautifulSoup

# Time keeping
from utils.timeit import timeit

from Article import Article

class LexisNexisHTMLParser():
	# Variables shared by all instances

	def __init__(self, fileName):
		# Variables specific to instance
		self.articles = [] # All articles

		# Parse the specified file
		self.parseFile(fileName)

	def parseFile(self, fileName):
		f = open(fileName)
		html = BeautifulSoup(f, 'html.parser')

		allAelements = html.find_all('a')

		for el in allAelements:
			divs = el.find_all_next('div', limit=7)

			# Create the article data
			journal = divs[1].get_text()
			link = divs[2].get_text()
			date = divs[3].get_text()
			title = divs[4].get_text()
			text = divs[6].get_text()

			# Add the article
			self.articles.append(Article(title, text, journal, link, date))

	def getAllText(self):
		return [art.text for art in self.articles]

	def getAllTitles(self):
		return [art.title for art in self.articles]
