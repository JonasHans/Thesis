# Pandas
import pandas as pd
pd.set_option('display.expand_frame_repr', False) # show all collumns

import matplotlib.pyplot as plt
import numpy as np
import time
from utils.timeit import timeit

# Unique identifier for one run which can be used to match results
UNIQUE_IDENTIFIER = str(int(time.time()))

def analyzeBRON(bron):
	global UNIQUE_IDENTIFIER
	total = 0
	filled = 0
	percentages = []

	for feature in bron:
		# Get lengths
		featureLen = len(bron[feature])
		filledLen = len(bron[bron[feature].notnull()])

		# Add to counters
		total += featureLen
		filled += filledLen

		percentages.append((filledLen/featureLen)*100)

	# Create bar plot of all features
	y_pos = np.arange(len(list(bron)))
	plt.barh(y_pos, percentages, align='center', alpha=0.5)
	plt.yticks(y_pos, list(bron))
	plt.yticks(fontsize=5)
	plt.savefig('../results/bronFeatureInfo-'+UNIQUE_IDENTIFIER+'.png')

	# Create bar plot of non null features
	nnPercentages = []
	nnLabels = []
	for i in range(0,len(percentages)):
		if percentages[i] != 0.0:
			nnPercentages.append(percentages[i])
			nnLabels.append(list(bron)[i])
	y_pos = np.arange(len(list(nnLabels)))
	plt.clf()
	plt.barh(y_pos, nnPercentages, align='center', alpha=0.5)
	plt.yticks(y_pos, nnLabels)
	plt.yticks(fontsize=6)
	plt.savefig('../results/bronFilledFeatureInfo-'+UNIQUE_IDENTIFIER+'.png')

	print('Number of features: ',len(list(bron)))
	print('Total number of fields: ',total)
	print('Total filled in: ',filled)
	print('Percentage: ', (filled/total)*100)

# shows information on result set
def queryResultsInfo(fileName, results):
	global UNIQUE_IDENTIFIER

	# Print feature information
	f = open('../results/'+fileName+'-'+UNIQUE_IDENTIFIER+'.txt', "a")
	f.write("Total number of features: "+str(len(list(results))) + "\n")
	f.write("Feature names: \n")
	for i in range(0, len(list(results)), 5):
		f.write(str(list(results)[i:i+5]) + '\n')

	# Gather stats on results
	stats = results.describe()

	# Result set information
	f.write('\n')
	f.write('Total number of results: ' + str(len(results)) + '\n')
	results.head(25).to_csv(f)
	# stats.to_csv(f)
	# f.write(stats)

@timeit
# Method which returns all results associated with the query
def queryBRON(bron_ongevallen, query):
	qString = ''

	# Build query string
	for term in query:
		if qString == '':
			qString = term + '==\"' + query[term] + '\"'
		else:
			qString += ' & '+ term + '==\"' + query[term] + '\"'

	# Execute query on the set
	return bron_ongevallen.query(qString)

@timeit
def indexBRON():
	# Read in the BRON ongevallen.txt
	# TODO: Define dtypes
	# dropna => axis=1 means we look at the columns, how=all means we only drop the column if all values are NaN
	# fillna all NaN values to zero
	return [
		pd.read_csv('../data/BRON2017/gegevens/Ongevallengegevens/ongevallen.txt', sep=',', index_col='VKL_NUMMER', low_memory=False).dropna(axis=1, how='all').fillna(value=0)
		]

@timeit
def main():
	# Index BRON dataset
	[bron_ongevallen] = indexBRON()

	# Analyse the BRON ongevallen dataset
	# analyzeBRON(bron_ongevallen)

	# Query the dataset
	query = {
		'MND_NUMMER' : str(12),
		'AP3_CODE' : 'DOD'
	}

	# Write query object to file
	f = open('../results/queryBron-'+UNIQUE_IDENTIFIER+'.txt', "w")
	f.write('Query : ' + str(query) + '\n\n')
	f.close()

	# Execte query
	qResult = queryBRON(bron_ongevallen, query)
	print(qResult.loc[:,['JAAR_VKL','MND_NUMMER','UUR','DAGTYPE','GME_NAAM','AP3_CODE']])
	queryResultsInfo('queryBron', qResult)

if __name__== "__main__":
	main()
