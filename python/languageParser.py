import spacy
import nltk
from nltk.corpus import stopwords

# Time keeping
from utils.timeit import timeit

# Default language parser is spacy
@timeit
class LanguageParser():
	nlp = spacy.load('nl_core_news_sm')

	def __init__(self, parser='spacy'):
		self.parser = parser

	def getWordsLen(self, text):
		return len(self.NLTKremoveStopwords(nltk.word_tokenize(text)))

	# Dependency parser for data
	def DEP(self, data, cleanData):
		deps = []

		# Remove stopwords and other symbols if configured to remove
		if cleanData:
			data = " ".join(self.NLTKremoveStopwords(nltk.word_tokenize(data)))

		# Spacy parses dependencies and nltk POS tags
		if self.parser == 'spacy':
			# deps = self.spacyDEP(data)
			deps = self.spacyPOS(data)
		elif self.parser == 'nltk':
			deps = self.nltkPOS(data, cleanData)

		return deps

	def sentences(self, text):
		return nltk.sent_tokenize(text)

	def doesTextContainTerm(self, text, goalToken):
		if self.parser == 'spacy':
			tokens = self.nlp(text)

			for token in tokens:
				if token.text == goalToken:
					return True

		return False
	# Filter sentences in a text to only return those matching the filter
	def filterTextInSentences(self, text, filter):
		if self.parser == 'spacy':
			doc = self.nlp(text)
			validSents = []

			for sent in doc.sents:
				if (filter[0] in str(sent)) and (filter[1] in str(sent)):
					validSents.append(str(sent))

			return validSents


	# Spacy dependencies method
	def spacyPOS(self, data):
		doc = self.nlp(data)

		return [(token.text, token.pos_) for token in doc]

	# Spacy dependencies method
	def spacyDEP(self, data):
		data = " ".join(self.NLTKlowerCaseTokens(nltk.word_tokenize(data)))
		doc = self.nlp(data)

		return [(token.text, token.dep_) for token in doc]

	# NLTK Pos tags method
	def nltkPOS(self, data, cleanData):
		tokens = nltk.word_tokenize(data)
		if cleanData:
			tokens = self.NLTKremoveStopwords(tokens)

		return nltk.pos_tag(tokens)

	# NLTK token cleansing method which removes stopwords, non alpha words and digits
	def NLTKremoveStopwords(self, tokens):
		tokens = self.NLTKlowerCaseTokens(tokens)
		return list(filter(lambda word: (word.lower() not in stopwords.words('dutch')) and (word.isalpha() or word.isdigit()) ,tokens))

	# Method which lowercases tokens
	def NLTKlowerCaseTokens(self, tokens):
		return [token.lower() for token in tokens]
