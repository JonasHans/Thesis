import time
import pprint
import pandas as pd

# Time keeping
from utils.timeit import timeit

# Traffic Accident News Analyser
@timeit
class TANA():
	features = ['text', 'title']
	pp = pprint.PrettyPrinter(indent=4)

	def __init__(self, IR, loadIRdependencies, loadAnalytics):
		self.IR = IR

		# Load/create IR dependencies
		for f in self.features:
			if loadIRdependencies:
				self.IR.loadDataFrame(f)
			else:
				self.IR.createDependencies(f)
				self.IR.writeDataFrame(f)

	##########################
	#### ANALYSIS METHODS ####
	##########################

	@timeit
	def dataStats(self):
		# Create a file for the stats to be printed in
		resultFile = open('../results/dataStats-'+str(time.time())+'.txt', 'x')

		# General stats (some stats only show if not loaded)
		resultFile.write('Total number of articles: '+str(len(self.IR.data.articles))+'\n')
		resultFile.write('Total number of unique articles: '+str(len(self.IR.df))+'\n')
		resultFile.write('Diversity of article formats in HTML:'+'\n')
		resultFile.write(self.pp.pformat(self.IR.data.infoCounts)+'\n')

		for feat in self.features:
			resultFile.write('************ Most common words in '+feat+' feature **********************'+'\n')
			resultFile.write(str(self.rankListBySum(self.IR.dependencies[feat]).head(50))+'\n')
			resultFile.write('\n')

		resultFile.close()

	##########################
	#### HELPER METHODS ######
	##########################

	def dependencyAnalysis(self, feature, mainTerm, secondaryTerm):
		self.IR.sentenceDepencyRelations()

	# ir.dependencies['text']
	def rankListBySum(self, toRank):
		toRank['sum'] = pd.Series(toRank.sum(axis=1), index=toRank.index)
		return toRank.sort_values(by='sum', ascending=False)
