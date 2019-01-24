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
	spacyParser = LanguageParser(parser='nltk')

	# Configure information retrieval
	ir = InformationRetrieval(spacyParser, data)

	# Traffic accident news analyser
	analyzer = TANA(ir, loadIRdependencies, loadAnalytics)

	# Basic statistics of the data
	# analyzer.dataStats()

	# analyzer.patternAnalysis()

	# analyzer.plotDependencies()
	analyzer.dataPlots()


if __name__== "__main__":
	main()
