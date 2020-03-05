#!/usr/bin/env python
# coding: utf-8

import os

from scrapy.crawler import CrawlerProcess
from Spiders.Wikipedia import Spider
from gensim.corpora import Dictionary
from WikiSpaCyCorpus import WikiSpacyCorpus

# Scrape Metacritic
process = CrawlerProcess(settings={
    "FEED_FORMAT": "json",
    "FEED_URI": "Data/Games.json",
    "COOKIES_ENABLED": "False",
    "LOG_LEVEL": "WARNING",
})

#process.crawl(Spider)
#process.start()

# If dictionary was already created, load it
# Otherwise ensure that the variable is kept as None (as expected by Gensim)
path_dictionary = "Data/GamesBOW.txt"
dictionary = Dictionary.load_from_text(path_dictionary) if os.path.exists(path_dictionary) else None

# Note that the input attribute needs to be manually set
wiki = WikiSpacyCorpus("Data/Games.xml.bz2", article_min_tokens=200, dictionary=dictionary)
setattr(wiki, "input", wiki.fname)

if not os.path.exists(path_dictionary):
    wiki.dictionary.filter_extremes(no_below=20, no_above=0.1)
    dictionary = wiki.dictionary
    dictionary.save_as_text(path_dictionary, False)

# Get tokens from each page
# Replace generator with list for accessibility
pages = list(wiki.get_texts())
