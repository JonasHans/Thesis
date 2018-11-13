# Rss feed
import feedparser

# Web page scraping
from lxml import html
import requests
COOKIES = dict(BCPermissionLevel='PERSONAL')

# NLTK
import nltk
from nltk.corpus import stopwords

# Counter
from collections import Counter

tokens = []
tokensTitle = []

def parseFeed(rssFeed):
    feed = feedparser.parse(rssFeed)
    global tokens,tokensTitle

    # Go through all xml items
    for item in feed["items"]:
        link = item["link"]
        title = item["title"]
        # Scrape the linked webpage
        page = requests.get(link, cookies=COOKIES)
        tree = html.fromstring(page.content)

        # Get the paragraphs
        paragraphs = tree.xpath('//p[.//text()]/text()')
        paragraphs = " ".join(paragraphs)

        # Tokenize
        word_list = nltk.tokenize.word_tokenize(paragraphs)
        filtered_words = [word.lower() for word in word_list if word.lower() not in stopwords.words('dutch')]
        tokens = tokens + filtered_words

        word_list2 = nltk.tokenize.word_tokenize(title)
        filtered_words2 = [word.lower() for word in word_list2 if word.lower() not in stopwords.words('dutch')]
        tokensTitle = tokensTitle + filtered_words2

def main():
    global tokens

    # Trefwoorden
    text_file = open("../data/trefwoorden.txt", "r")
    trefwoorden = text_file.read().split('\n')
    print(trefwoorden)

    for woord in trefwoorden:
        parseFeed("https://news.google.com/news/rss/search/section/q/"+woord+"?gl=NL&hl=nl&ned=nl_nl&ceid=NL%3Anl")

    # Count tokens
    countTokens = Counter(tokens)
    with open('../results/paragraphs.txt', 'w') as f:
        for tup in countTokens.most_common(50):
            f.write(tup[0] + ' - ' + str(tup[1]) + '\n')


    countTokens2 = Counter(tokensTitle)
    with open('../results/titles.txt', 'w') as f:
        for tup in countTokens2.most_common(50):
            f.write(tup[0] + ' - ' + str(tup[1]) + '\n')

if __name__== "__main__":
    main()
