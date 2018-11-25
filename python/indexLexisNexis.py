# Pandas
import pandas as pd
pd.set_option('display.expand_frame_repr', False) # show all collumns

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

@timeit
def tokenizeText(fileText):
	# Tokenize to tokens and sentences
	tokens = nltk.word_tokenize(fileText)
	tokensClean = removeStopwords(tokens)
	sentences = nltk.sent_tokenize(fileText)

	return [tokens, tokensClean, sentences]

@timeit
def querySentences(query, sentences):
	# result = []
	# for sent in sentences:
	# 	print(sent)
	# 	if all(elem in sent for elem in query):
	# 		result.append(sentences[sent])
	# return result
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

@timeit
def lowerCaseTokens(tokens):
	return [token.lower() for token in tokens]

@timeit
def trigramToken(token, pos, trigrams):
	if pos == -1:
		return list(filter(lambda trigram: token in list(trigram), trigrams))
	else:
		return list(filter(lambda trigram: trigram[pos] == token, trigrams))

@timeit
def removeStopwords(tokens):
	tokens = lowerCaseTokens(tokens)
	return list(filter(lambda word: (word.lower() not in stopwords.words('dutch')) and (word.isalpha() or word.isdigit())  ,tokens))

@timeit
def main():
	# articles = indexLexisNexis()
	data = LexisNexisHTMLParser('../data/html#1.HTML')
	# print(data.getAllTitles())
	[tokens, tokensClean, sentences] = tokenizeText(data.getAllTitles())
	trigram(tokensClean)
	# printList(querySentences(['geschept'], sentences))
	# namedEntityRecognition(sentences)

if __name__== "__main__":
	main()
