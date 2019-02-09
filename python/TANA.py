import time
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy as np
import seaborn as sns

# Time keeping
from utils.timeit import timeit

# Traffic Accident News Analyser
@timeit
class TANA():
	features = ['text', 'title']
	pp = pprint.PrettyPrinter(indent=4)
	objects = [
		'auto'
		# 'vrachtwagen',
		# 'motorrijder',
		# 'trein',
		# 'fiets'
	]

	persons = [
		'geschept'
		# 'fietser',
		# 'man',
		# 'vrouw',
		# 'fietsster',
		# 'voetganger'
	]


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

	def dataPlots(self):
		# Journal plots
		# self.IR.df['journal'].value_counts().head(20).plot(kind='barh')
		# plt.savefig('../plots/journal.png')
		# plt.tight_layout()
		# plt.savefig('../plots/journalLabels.png')
		# plt.close()
		#
		# self.IR.df['journal'].value_counts().value_counts().sort_index().plot(kind='barh', fontsize=6)
		# plt.xlabel('Frequency')
		# plt.ylabel('Amount of articles per journal')
		# plt.savefig('../plots/journalHist.png')
		# plt.clf()

		# Date plot
		# self.IR.df["date"] = self.IR.df["date"].astype("datetime64")
		# self.IR.df["date"].groupby([self.IR.df["date"].dt.year]).count().plot(kind="bar")
		# plt.xlabel('Year')
		# plt.ylabel('Amount of articles')
		# plt.tight_layout()
		# plt.savefig('../plots/articleDates.png')

		# KDE plot of title and text length
		# [titles, texts] = self.IR.calcLengths()
		# tpf = pd.DataFrame(titles)
		# tpf.plot(kind='kde', legend=False)
		# plt.xlabel('Amount of words')
		# plt.savefig('../plots/titleLen.png')
		# plt.clf()
		#
		# textpf = pd.DataFrame(texts)
		# textpf.plot(kind='kde', legend=False)
		# plt.xlabel('Amount of words')
		# plt.savefig('../plots/textLen.png')
		# plt.clf()

		# sns.set_style('darkgrid')
		# plt2 = sns.distplot(titles, kde=True, hist=True)
		# plt2.set(xlabel='Amount of words')
		# plt2.get_figure().savefig('../plots/seabornTitles.png')
		# plt.clf()
		#
		# sns.set_style('darkgrid')
		# plt2 = sns.distplot(texts, kde=True, hist=True)
		# plt2.set(xlim=(0, 400))
		# plt2.set(xlabel='Amount of words')
		# plt2.get_figure().savefig('../plots/seabornText.png')

		# POS tags plot
		# self.IR.dependencies['title']['NOUN'].sort_values().tail(25).plot(kind='barh')
		# # self.rankListBySum(self.IR.dependencies['title'][['NN','NNP','NNS']])['sum'].head(25).plot(kind='barh')
		# plt.tight_layout()
		# plt.savefig('../plots/titlePOS-NN.png')
		# plt.close()
		#
		# self.IR.dependencies['title']['ADJ'].sort_values().tail(25).plot(kind='barh')
		# # self.rankListBySum(self.IR.dependencies['title'][['JJ','JJR','JJS']])['sum'].head(25).plot(kind='barh')
		# plt.tight_layout()
		# plt.savefig('../plots/titlePOS-JJ.png')
		# plt.close()
		#
		# self.IR.dependencies['title']['VERB'].sort_values().tail(25).plot(kind='barh')
		# # self.rankListBySum(self.IR.dependencies['title'][['VB','VBD','VBG','VBN','VBP','VBZ']])['sum'].head(25).plot(kind='barh')
		# plt.tight_layout()
		# plt.savefig('../plots/titlePOS-VB.png')
		# plt.close()
		#
		# self.IR.dependencies['text']['NOUN'].sort_values().tail(25).plot(kind='barh')
		# # self.rankListBySum(self.IR.dependencies['text'][['NN','NNP','NNS']])['sum'].head(25).plot(kind='barh')
		# plt.tight_layout()
		# plt.savefig('../plots/textPOS-NN.png')
		# plt.close()
		#
		# self.IR.dependencies['text']['ADJ'].sort_values().tail(25).plot(kind='barh')
		# # self.rankListBySum(self.IR.dependencies['text'][['JJ','JJR','JJS']])['sum'].head(25).plot(kind='barh')
		# plt.tight_layout()
		# plt.savefig('../plots/textPOS-JJ.png')
		# plt.close()
		#
		# self.IR.dependencies['text']['VERB'].sort_values().tail(25).plot(kind='barh')
		# # self.rankListBySum(self.IR.dependencies['text'][['JJ','JJR','JJS']])['sum'].head(25).plot(kind='barh')
		# plt.tight_layout()
		# plt.savefig('../plots/textPOS-VB.png')
		# plt.close()
		print()

	@timeit
	def dataStats(self):
		# Create a file for the stats to be printed in
		resultFile = open('../results/dataStats-'+str(time.time())+'.txt', 'x')

		# General stats (some stats only show if not loaded)
		resultFile.write('Total number of articles: '+str(len(self.IR.data.articles))+'\n')
		resultFile.write('Total number of unique articles: '+str(len(self.IR.df))+'\n')
		resultFile.write('Diversity of article formats in HTML:'+'\n')
		resultFile.write(self.pp.pformat(self.IR.data.infoCounts)+'\n')

		# Feature dependencies
		for feat in self.features:
			resultFile.write('************ Most common words in '+feat+' feature **********************'+'\n')
			resultFile.write(str(self.rankListBySum(self.IR.dependencies[feat]).head(50))+'\n')
			resultFile.write('\n')

			resultFile.write('************ Sum of objects and person in feature **********************'+'\n')
			# Counts of objects and persons
			for obj in self.objects:
				resultFile.write(obj+': '+str(self.IR.dependencies[feat].loc[obj]['sum'])+'\n')
			for person in self.persons:
				resultFile.write(person+': '+str(self.IR.dependencies[feat].loc[person]['sum'])+'\n')

		# Occurences of multiple terms together
		# for obj in self.objects:
		# 	for person in self.persons:
		# 		resultFile.write(obj+'-'+person+': '+str(self.IR.countOccurences('title', [obj, person], True))+'\n')

		# Create subset of terms
		# resultFile.write('************ Text dependencies auto **********************'+'\n')
		# resultFile.write(self.pp.pformat(self.IR.createSubset('text', ['auto'], ['fietser', 'man', 'vrouw'], '../frames/subsetTextAutoFMV'))+'\n')

		# resultFile.write('************ Text dependencies all **********************'+'\n')
		# resultFile.write(self.pp.pformat(self.IR.createSubset('text', self.objects, self.persons, '../frames/subsetTextVRU'))+'\n')

		# resultFile.write('************ Title dependencies all **********************'+'\n')
		# resultFile.write(self.pp.pformat(self.IR.createSubset('title', self.objects, self.persons, '../frames/subsetTitleAllNLTK'))+'\n')

		# self.IR.createSubset('text', ['auto'], ['fietser'], '../frames/test')

		resultFile.close()

	##########################
	#### HELPER METHODS ######
	##########################

	def plotDependencies(self):
		deps = pickle.load(open( "../frames/subsetTextAll.pkl", "rb" ))

		for mainTerm in deps:
			a = []
			b = []
			for tup in deps[mainTerm].most_common(10):
				a.append(str(tup[0]))
				b.append(tup[1])

			y_pos = np.arange(len(a))
			plt.barh(y_pos, b, align='center', alpha=0.5)
			plt.yticks(y_pos, a)
			plt.yticks(fontsize=5)
			plt.savefig('../results/depsFig-'+str(mainTerm)+'.png')
			plt.clf()

	def dependencyAnalysis(self, feature, mainTerm, secondaryTerm):
		self.IR.sentenceDepencyRelations()

	# ir.dependencies['text']
	def rankListBySum(self, toRank):
		toRank['sum'] = pd.Series(toRank.sum(axis=1), index=toRank.index)
		return toRank.sort_values(by='sum', ascending=False)

	def patternAnalysis(self):
		# Plot auto geschept
		# [deps, subs, obls] = self.IR.extractPattern('title', ['geschept'])
		# self.plotCounter(subs, 'stap5-nsubj-Dist1-aangereden')
		# self.plotCounter(obls, 'stap5-obl-Dist1-aangereden')

		[subs, obl, roots] = self.IR.extractPattern2('title')
		# self.plotCounter(subs, 'stap6-general-nsub-dist')
		# self.plotCounter(obl, 'stap6-general-obl-dist')
		# self.plotCounter(roots, 'stap6-general-obl-roots')
		# self.IR.nounChunker('title')

	def plotCounter(self, c, name):
		labels, values = zip(*c)
		indexes = np.arange(len(labels))
		width = 0.75

		plt.barh(indexes, values, width, align='edge')
		plt.yticks(indexes + width * 0.5, labels)
		plt.subplots_adjust(left=0.2)
		plt.savefig('../plots/'+name+'.png')
		plt.close()
