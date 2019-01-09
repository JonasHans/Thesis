# Python libs
from collections import Counter
import pickle

# Pandas
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Time keeping
from utils.timeit import timeit

# Custom classes
from lexisNexisHTMLParser import LexisNexisHTMLParser
from languageParser import LanguageParser
from informationRetrieval import InformationRetrieval
from TANA import TANA

@timeit
def main():
	# Load variables
	loadLexisNexis = True
	loadIRdependencies = True
	loadAnalytics = True

	# Read in dataset of lexis nexis articles
	data = LexisNexisHTMLParser(loadLexisNexis)

	# Define language parser
	spacyParser = LanguageParser(parser='spacy')

	# Configure information retrieval
	ir = InformationRetrieval(spacyParser, data)

	# Traffic accident news analyser
	analyzer = TANA(ir, loadIRdependencies, loadAnalytics)

	# Basic statistics of the data
	analyzer.dataStats()

def categoriesInfo():
	cats = pickle.load(open( "categories.pkl", "rb" ))
	print(cats)
	for key in cats:
		if key[0] == 'auto':
			print(key)
			for x in Counter(cats[key]).most_common():
				print(x)
			print()

def ir(data):
	# Spacy parser
	spacyParser = LanguageParser(parser='spacy')

	# Information retrieval
	loadIR = True
	ir = InformationRetrieval(spacyParser, data)
	if (loadIR):
		ir.loadDataFrame('title')
	else:
		ir.createDependencies('title')
		ir.writeDataFrames()

	# ir.sentenceDepencyRelations()
	print('auto: ', len(ir.countOccurences('title', ['automobilist'])))
	print('fiets: ',len(ir.countOccurences('title', ['fiets'])))
	print('auto-fiets: ',len(ir.countOccurences('title', ['auto','fiets'])))

	# ir.countOccurences('text', ['auto'])
	# ir.countOccurences('text', ['fiets'])
	# ir.countOccurences('text', ['auto','fiets'])

	# print(ir.dependencies['text'].loc['auto'])
	# print(ir.dependencies['text'].loc['automobilist'])
	# print(ir.dependencies['text'].loc['fiets'])
	# print(ir.dependencies['text'].loc['fietser'])

if __name__== "__main__":
	main()
