import spacy
import nltk
from nltk.corpus import stopwords

# Default language parser is spacy
class LanguageParser():
	nlp = spacy.load('nl_core_news_sm')

	def __init__(self, parser='spacy'):
		self.parser = parser

	def DEP(self, data, cleanData):
		deps = []
		if cleanData:
			data = " ".join(self.NLTKremoveStopwords(nltk.word_tokenize(data)))

		if self.parser == 'spacy':
			deps = self.spacyDEP(data)
		elif self.parser == 'nltk':
			deps = self.nltkPOS(data, cleanData)

		return deps

	def filterTextInSentences(self, text, filter):
		if self.parser == 'spacy':
			doc = self.nlp(text)
			validSents = []

			for sent in doc.sents:
				if (filter[0] in str(sent)) and (filter[1] in str(sent)):
					validSents.append(str(sent))

			return validSents

	def spacyDEP(self, data):
		doc = self.nlp(data)

		return [(token.text, token.dep_) for token in doc]

	def nltkPOS(self, data, cleanData):
		tokens = nltk.word_tokenize(data)
		if cleanData:
			tokens = self.NLTKremoveStopwords(tokens)

		return nltk.pos_tag(tokens)

	def NLTKremoveStopwords(self, tokens):
		tokens = self.NLTKlowerCaseTokens(tokens)
		return list(filter(lambda word: (word.lower() not in stopwords.words('dutch')) and (word.isalpha() or word.isdigit()) ,tokens))

	def NLTKlowerCaseTokens(self, tokens):
		return [token.lower() for token in tokens]
