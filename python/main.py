# Python libs
from collections import Counter

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
	loadLexisNexis = True
	data = LexisNexisHTMLParser(loadLexisNexis)
	# print(data.dataFrame)
	# print(data.dataFrame.describe())
	ir(data)

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

	# print(ir.dependencies['title'].loc['auto'])
	# print(ir.dependencies['title'].loc['Fietser'])
	# print(ir.dependencies['title'].loc['fietser'])
	# print(ir.dependencies['title'].loc['Fietsster'])

	ir.dependencies['text']['sum'] = pd.Series(ir.dependencies['text'].sum(axis=1), index=ir.dependencies['text'].index)
	print(ir.dependencies['text'].sort_values(by='sum', ascending=False))

if __name__== "__main__":
	main()
