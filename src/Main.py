#!/usr/bin/env python
# coding: utf-8

from scrapy.crawler import CrawlerProcess
from Spiders.Wikipedia import Spider
from gensim.corpora import WikiCorpus, dictionary, MmCorpus

# Scrape Metacritic
process = CrawlerProcess(settings={
    "FEED_FORMAT": "json",
    "FEED_URI": "Data/Games.json",
    "COOKIES_ENABLED": "False",
    "LOG_LEVEL": "WARNING",
})

#process.crawl(Spider)
#process.start()

wiki = WikiCorpus("Data/Games.xml.bz2", lemmatize=False, article_min_tokens=200)
wiki.dictionary.filter_extremes(no_below=20, no_above=0.1)
wiki.dictionary.save_as_text("Data/GamesBOW.txt", False)
