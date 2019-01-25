# Generic python libs
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import datefinder

# Time keeping
from utils.timeit import timeit

# Custom classes
from Article import Article

# Class which parses lexis nexis html article downloads into a python class
@timeit
class LexisNexisHTMLParser():
	# Variables shared by all instances
	index = 0
	infoCounts = []

	def __init__(self, load):
		# Variables specific to instance
		self.articles = {} # All articles
		self.dataFrame = None

		if (load):
			self.loadDataFrame()
		else:
			# Parse the data directory
			self.parseDataDirectory()

			# create dataframe
			self.createDataFrame()

			# clean data (remove all duplicate articles)
			self.dataFrame = self.dataFrame.drop_duplicates(subset='text')

			# Write dataframe
			self.writeDataFrame()

	@timeit
	def parseDataDirectory(self):
		self.parseFile('../data/aangereden_1-200.HTML', 'aangereden')
		self.parseFile('../data/aangereden_201-400.HTML', 'aangereden')
		self.parseFile('../data/aanrijding_1-200.HTML', 'aanrijding')
		self.parseFile('../data/aanrijding_201-400.HTML', 'aanrijding')
		self.parseFile('../data/ongeluk_1-200.HTML', 'ongeluk')
		self.parseFile('../data/ongeluk_201-400.HTML', 'ongeluk')
		self.parseFile('../data/botsing_1-200.HTML', 'botsing')
		self.parseFile('../data/botsing_201-400.HTML', 'botsing')
		self.parseFile('../data/botsing_401-600.HTML', 'botsing')
		self.parseFile('../data/geschept_1-200.HTML', 'geschept')
		self.parseFile('../data/geschept_201-400.HTML', 'geschept')
		self.parseFile('../data/geschept_401-600.HTML', 'geschept')
		self.parseFile('../data/ongeval_1-200.HTML', 'ongeval')
		self.parseFile('../data/ongeval_201-400.HTML', 'ongeval')
		self.parseFile('../data/ongeval_401-600.HTML', 'ongeval')
		# print("Divs count in documents: ", Counter(self.infoCounts))

	@timeit
	def parseFile(self, fileName, setLabel):
		# Open the file with html structured articles
		f = open(fileName)
		html = BeautifulSoup(f, 'html.parser')

		# Find all 'a' elements which correspond to individual articles
		allAelements = html.find_all('a')

		# Go through all articles and structure each article into features
		for el in allAelements:

			# Calculate the amount of divs this article contains (6 variants)
			divs = []
			for sibling in el.next_siblings:
				if sibling.name == 'a':
					break
				elif sibling.name == 'div':
					divs.append(sibling)
			self.infoCounts.append(len(divs))

			# Select biggest div as text
			size = 0
			for div in divs:
				if len(div.get_text()) > size:
					biggestDiv = div
					size = len(div.get_text())
			text = biggestDiv.get_text()

			# Article contains 7 divs
			if len(divs) == 7:
				# Create the article data
				journal = divs[1].get_text()
				link = divs[2].get_text()
				date = next(datefinder.find_dates(divs[3].get_text()))
				title = divs[4].get_text()
			else:
				# Create the article data
				journal = divs[len(divs)-1].get_text()
				link = divs[1].get_text()
				date = next(datefinder.find_dates(divs[2].get_text()), None)
				title = divs[3].get_text()

			# Add the article
			article = Article(title, text, journal, link, date, setLabel)
			self.articles[self.index] = article.getArticle()
			self.index += 1

	def createDataFrame(self):
		self.dataFrame = pd.DataFrame(self.articles).transpose()

	def writeDataFrame(self):
		self.dataFrame.to_pickle("../frames/lexisNexis.pkl")

	def loadDataFrame(self):
		self.dataFrame = pd.read_pickle('../frames/lexisNexis.pkl')

	def getAllText(self):
		return [art.text for art in self.articles]

	def getAllTitles(self):
		return [art.title for art in self.articles]
