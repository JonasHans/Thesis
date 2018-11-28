from bs4 import BeautifulSoup
import uuid
import pandas as pd

# Time keeping
from utils.timeit import timeit

from Article import Article

class LexisNexisHTMLParser():
	# Variables shared by all instances

	def __init__(self, fileName, df):
		# Variables specific to instance
		self.articles = {} # All articles
		self.dataFrame = None

		# Parse the specified file
		self.parseFile(fileName)

		# create dataframe if true
		if (df):
			self.createDataFrame()

	@timeit
	def parseFile(self, fileName):
		f = open(fileName)
		html = BeautifulSoup(f, 'html.parser')
		index = 0

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
			article = Article(title, text, journal, link, date)
			self.articles[index] = article.getArticle()
			index += 1

	@timeit
	def createDataFrame(self):
		self.dataFrame = pd.DataFrame(self.articles).transpose()

	def getAllText(self):
		return [art.text for art in self.articles]

	def getAllTitles(self):
		return [art.title for art in self.articles]
