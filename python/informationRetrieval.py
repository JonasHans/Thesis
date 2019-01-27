import pandas as pd
import pickle
from collections import Counter
import pprint

# Time keeping
from utils.timeit import timeit

import nltk

# General information retrieval class
@timeit
class InformationRetrieval():
	pp = pprint.PrettyPrinter(indent=4)

	def __init__(self, parser, data):
		self.parser = parser
		self.data = data
		self.df = data.dataFrame
		self.dependencies = {}

	def calcLengths(self):
		progress = 100
		titles = []
		texts = []

		for index, row in self.df.iterrows():
			textLen = self.parser.getWordsLen(row['text'])
			titleLen = self.parser.getWordsLen(row['title'])

			# Output progress through set
			if ((index%100) == 0):
				print('Progress: '+str(progress)+'/'+str(len(self.df)))
				progress += 100

			titles.append(titleLen)
			texts.append(textLen)

		return [titles, texts]

	def nounChunker(self, feature):
		grammar = "NP: {<DT>?<JJ>*<NN>}"
		progress = 100

		for index, row in self.df.iterrows():
			text = row[feature]
			sentPOS = self.parser.nltkPOS(text, True)

			# Output progress through set
			if ((index%100) == 0):
				print('Progress: '+str(progress)+'/'+str(len(self.df)))
				progress += 100

			cp = nltk.RegexpParser(grammar)
			result = cp.parse(sentPOS)
			print(result)
			print()

	def extractPattern2(self, feature):
		progress = 100
		intersections = {}

		subjects = []
		roots = []
		obls = []
		count = 0
		for index, row in self.df.iterrows():
			text = row[feature]

			# Output progress through set
			if ((index%100) == 0):
				print('Progress: '+str(progress)+'/'+str(len(self.df)))
				progress += 100

			sentDEPS = self.parser.spacyDEP(text)

			sub = ''
			root = ''
			for dep in sentDEPS:
				if dep[1] == 'nsubj':
					sub = dep[0]
					subjects.append(dep[0])
				if dep[1] == 'ROOT':
					root = dep[0]
					roots.append(dep[0])
				if dep[1] == 'obl':
					obls.append(dep[0])

			if sub and root:
				count += 1
				if not sub in intersections:
					intersections[sub] = [root]
				else:
					intersections[sub].append(root)

		# for x in Counter(subjects).most_common(10):
		# 	print(x[0])
		# 	print(self.pp.pformat(Counter(intersections[x[0]]).most_common()))
		# print(count)
		# print(self.pp.pformat(Counter(subjects).most_common(10)))
		# print()
		# print(self.pp.pformat(Counter(roots).most_common(5)))
		return [Counter(subjects).most_common(15),Counter(obls).most_common(15),Counter(roots).most_common(15)]

	def extractPattern(self, feature, terms):
		counts = {
			'total' : 0,
			'valid' : 0
		}
		vru = []
		cause = []
		progress = 100
		nsubjs = []
		obls = []
		case = []

		deps = []
		for index, row in self.df.iterrows():
			text = row[feature]

			# Output progress through set
			if ((index%100) == 0):
				print('Progress: '+str(progress)+'/'+str(len(self.df)))
				progress += 100

			if feature == 'text':
				print('NOPE')
			else:
				# For efficieny we filter only relevant sentences
				if all(x in text for x in terms):
					counts['total'] += 1
					sentPOS = self.parser.nltkPOS(text, True)
					sentDEPS = self.parser.spacyDEP(text)
					key = ""
					val = ""

					# loop through depencies
					val = False
					subj = ""
					obl = ""
					for dep in sentDEPS:
						deps.append(dep[1])
						if (dep[1] == 'case'):
							case.append(dep[0])
						if (dep[1] == 'nsubj'):
							nsubjs.append(dep[0])
							subj = dep[0]
						if (dep[1] == 'obl'):
							obls.append(dep[0])
							obl = dep[0]
						if (dep[0] == 'geschept') and (dep[1] == 'ROOT'):
							# print(sentDEPS)
							val = True
					if val:
						counts['valid'] += 1
						vru.append(subj)
						cause.append(obl)
					else:
						print('not valid: ', text)
		return [Counter(deps).most_common(15),Counter(nsubjs).most_common(15),Counter(obls).most_common(15),Counter(case).most_common(15)]

	@timeit
	def createSubset(self, feature, mainTerms, secondaryTerms, fileName):
		progress = 100
		intersections = {}

		for index, row in self.df.iterrows():
			text = row[feature]

			# Output progress through set
			if ((index%100) == 0):
				print('Progress: '+str(progress)+'/'+str(len(self.df)))
				progress += 100

			if feature == 'text':
				sents = self.parser.sentences(text)

				for sent in sents:
					text = sent

					# For efficieny we filter only relevant sentences
					if any(x in text for x in mainTerms) and any(x in text for x in secondaryTerms):
						sentDeps = self.parser.DEP(text, True)
						sentSpac = self.parser.spacyDEP(text)
						key = ""
						val = ""

						# loop through depencies
						for dep in sentDeps:
							# Check for the main term
							for mterm in mainTerms:
								if mterm == dep[0]:
									key = dep

							# Check the secondary term
							for sterm in secondaryTerms:
								if sterm == dep[0]:
									val = dep

						# Check if valid key-value pair
						if key and val:
							# if 'VBG' in [x[1] for x in sentDeps]:
							print(sent)
							print(sentDeps)
							print(sentSpac)
							print()
							if not key in intersections:
								intersections[key] = [val]
							else:
								intersections[key].append(val)
			else:
				# For efficieny we filter only relevant sentences
				if any(x in text for x in mainTerms) and any(x in text for x in secondaryTerms):
					sentDeps = self.parser.DEP(text, True)
					sentSpac = self.parser.spacyDEP(text)
					key = ""
					val = ""

					# loop through depencies
					for dep in sentDeps:
						# Check for the main term
						for mterm in mainTerms:
							if mterm == dep[0]:
								key = dep

						# Check the secondary term
						for sterm in secondaryTerms:
							if sterm == dep[0]:
								val = dep

					# Check if valid key-value pair
					if key and val:
						# if 'VBG' in [x[1] for x in sentDeps]:
						print(text)
						print(sentDeps)
						print(sentSpac)
						print()
						if not key in intersections:
							intersections[key] = [val]
						else:
							intersections[key].append(val)
		for key in intersections:
			intersections[key] = Counter(intersections[key])

		pickle.dump( intersections, open( fileName+".pkl", "wb" ) )

		return intersections

	@timeit
	def countOccurences(self, feature, terms, exactMatch):
		occurences = []
		progress = 100
		for index, row in self.df.iterrows():
			if ((index%100) == 0):
				print('Progress: '+str(progress)+'/'+str(len(self.df)))
				progress += 100
			text = row[feature]

			validOccurence = True

			if not exactMatch:
				for term in terms:
					if not term in text:
						validOccurence = False
			else:
				for term in terms:
					if not self.parser.doesTextContainTerm(text, term):
						validOccurence = False

			if validOccurence:
				occurences.append(text)

		return occurences

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
			text = row['title']

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

	def writeDataFrame(self, dep):
		self.dependencies[dep].to_pickle("../frames/"+dep+'-dependenciesNLTK.pkl')

	def loadDataFrame(self, feature):
		self.dependencies[feature] = pd.read_pickle('../frames/'+feature+'-dependenciesNLTK.pkl')
