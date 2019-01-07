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

@timeit
def main():
	# Parse HTMl data
	# loadLexisNexis = True
	# data = LexisNexisHTMLParser(loadLexisNexis)
	# print(data.dataFrame.describe())

	# ir(data)

	categoriesInfo()

def categoriesInfo():
	cats = pickle.load(open( "categories.pkl", "rb" ))
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
		ir.loadDataFrame('text')
	else:
		ir.createDependencies('text')
		ir.writeDataFrames()

	# ir.sentenceDepencyRelations()

	# print(ir.dependencies['text'].loc['auto'])
	# print(ir.dependencies['text'].loc['automobilist'])
	# print(ir.dependencies['text'].loc['fiets'])
	# print(ir.dependencies['text'].loc['fietser'])

# ir.dependencies['text']
def rankListBySum(toRank):
	toRank['sum'] = pd.Series(toRank.sum(axis=1), index=toRank.index)
	print(toRank.sort_values(by='sum', ascending=False))

if __name__== "__main__":
	main()
