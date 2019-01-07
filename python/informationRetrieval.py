import pandas as pd
import pickle

# Time keeping
from utils.timeit import timeit

# General information retrieval class
class InformationRetrieval():

	def __init__(self, parser, data):
		self.parser = parser
		self.data = data
		self.df = data.dataFrame
		self.dependencies = {}

	@timeit
	def sentenceDepencyRelations(self):
		progress = 100

		# Select texts with specific vocab
		termsA = ['auto', 'fiets']

		# Categories
		categories = {}
		for index, row in self.df.iterrows():
			if ((index%100) == 0):
				print('Progress: '+str(progress)+'/'+str(len(self.df)))
				progress += 100
			text = row['text']

			# # select text which matches terms
			if (termsA[0] in text) and (termsA[1] in text):

				# select sentences which match terms
				sents = self.parser.filterTextInSentences(text, termsA)

				# If matching sents are found we analyze
				if sents:
					for sent in sents:
						# dependencies for a sentence
						sentDeps = self.parser.DEP(sent, True)

						# loop through depencies
						for dep in sentDeps:
							if 'auto' in dep[0]:
								key = dep
							if 'fiets' in dep[0]:
								val = dep

						if not key in categories:
							categories[key] = [val]
						else:
							categories[key].append(val)
					# i += 1

			# if i == 100:
			# 	break
		# for key in categories:
		# 	print(key, len(categories[key]))
		pickle.dump( categories, open( "categories.pkl", "wb" ) )

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
			text = row[feature]
			deps = deps + self.parser.DEP(text, True)

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
