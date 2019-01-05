import pandas as pd

# Time keeping
from utils.timeit import timeit

# General information retrieval class
class InformationRetrieval():

	def __init__(self, parser, data):
		self.parser = parser
		self.data = data
		self.dependencies = {}

	@timeit
	def createDependencies(self, feature):
		depCounts = {}
		deps = []
		progress = 100

		# Get the dataframe
		for index, row in self.data.dataFrame.iterrows():
			if ((index%100) == 0):
				print('Progress: '+str(progress)+'/'+str(len(self.data.dataFrame)))
				progress += 100
			titleText = row[feature]
			deps = deps + self.parser.DEP(titleText)

		for tup in deps:
			if tup[0] in depCounts:
				if tup[1] in depCounts[tup[0]]:
					depCounts[tup[0]][tup[1]] += 1
				else:
					depCounts[tup[0]][tup[1]] = 1
			else:
				depCounts[tup[0]] = {
					tup[1] : 1
				}

		self.dependencies[feature] = pd.DataFrame(depCounts).transpose().fillna(value=0)

	def writeDataFrames(self):
		for dep in self.dependencies:
			self.dependencies[dep].to_pickle("../frames/"+dep+'-dependencies.pkl')

	def loadDataFrame(self, feature):
		self.dependencies[feature] = pd.read_pickle('../frames/'+feature+'-dependencies.pkl')
