# Pandas
import pandas as pd
pd.set_option('display.expand_frame_repr', False) # show all collumns

import sys

# Time keeping
from utils.timeit import timeit

# NLTK
import nltk
from nltk.corpus import stopwords

# Counter
from collections import Counter

# Lexis nexis html
from lexisNexisHTMLParser import LexisNexisHTMLParser

@timeit
def indexLexisNexis():
	# dropna => axis=1 means we look at the columns, how=all means we only drop the column if all values are NaN
	# fillna all NaN values to zero
	return pd.concat([
		pd.read_csv('../data/2017-01#1.CSV', sep=',', low_memory=False).dropna(axis=1, how='all').fillna(value=0),
		pd.read_csv('../data/2017-01#2.CSV', sep=',', low_memory=False).dropna(axis=1, how='all').fillna(value=0),
		pd.read_csv('../data/2017-01#3.CSV', sep=',', low_memory=False).dropna(axis=1, how='all').fillna(value=0)
		], sort=True)

def printList(l):
	print("***************")
	for i in l:
		print(i)
	print("***************")


def tokenizeText(fileText):
	# Tokenize to tokens and sentences
	tokens = nltk.word_tokenize(fileText)
	tokensClean = removeStopwords(tokens)
	sentences = nltk.sent_tokenize(fileText)

	return [tokens, tokensClean, sentences]

def querySentences(query, sentences):
	return list(filter(lambda sent: all(elem in sent for elem in query),sentences))


@timeit
def namedEntityRecognition(sentences):
	posTags = nltk.pos_tag(sentences)
	# printList(list(filter(lambda x: x[0] == 'auto',posTags)))
	# Named Entity Recognition
	# nltk.ne_chunk(sentences)

@timeit
def trigram(tokens):
	# Trigrams
	trigrams = nltk.trigrams(tokens)
	geschept = trigramToken('geschept', 1, trigrams)
	printList(Counter(geschept).most_common(15))

@timeit
def frequencyInfo(tokens):
	# Frequency distribution
	fd = nltk.FreqDist(tokens)
	printList(fd.most_common(50))


def lowerCaseTokens(tokens):
	return [token.lower() for token in tokens]

def trigramToken(token, pos, trigrams):
	if pos == -1:
		return list(filter(lambda trigram: token in list(trigram), trigrams))
	else:
		return list(filter(lambda trigram: trigram[pos] == token, trigrams))


def removeStopwords(tokens):
	tokens = lowerCaseTokens(tokens)
	return list(filter(lambda word: (word.lower() not in stopwords.words('dutch')) and (word.isalpha() or word.isdigit())  ,tokens))

@timeit
# Method which returns all results associated with the query
def queryDataFrame(dataFrame, query):
	# results = data.dataFrame[data.dataFrame['journal'].str.contains("Algemeen")]
	qString = ''

	# Build query string
	for term in query:
		if qString == '':
			qString = term + '==\"' + query[term] + '\"'
		else:
			qString += ' & '+ term + '==\"' + query[term] + '\"'

	# Execute query on the set
	return dataFrame.query(qString)

@timeit
def main():
	data = LexisNexisHTMLParser('../data/html#1.HTML', True)

	ongevallen = {}
	for index, row in data.dataFrame.iterrows():
		[tokens, tokensClean, sentences] = tokenizeText(row['title'])
		result = querySentences(['geschept'], tokensClean)

		if (result):
			ongevallen['V'] = result[0][0]

			print(trigram(tokensClean))

	# [tokens, tokensClean, sentences] = tokenizeText("".join(data.dataFrame['text']))
	# trigram(tokensClean)

	# printList(querySentences(['geschept'], sentences))
	# namedEntityRecognition(sentences)

if __name__== "__main__":
	main()
