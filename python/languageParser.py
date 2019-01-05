import spacy

# Default language parser is spacy
class LanguageParser():
	nlp = spacy.load('nl_core_news_sm')

	def __init__(self, parser='spacy'):
		self.parser = parser

	def DEP(self, data):
		deps = []

		if self.parser == 'spacy':
			deps = self.spacyDEP(data)

		return deps

	def spacyDEP(self, data):
		doc = self.nlp(data)

		return [(token.text, token.dep_) for token in doc]
