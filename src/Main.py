#!/usr/bin/env python
# coding: utf-8

import os, json, pickle

from Helpers.DataManager import DataManager
from scrapy.crawler import CrawlerProcess
from Spiders.Wikipedia import WikipediaSpider
from Spiders.Metacritic import MetacriticSpider
from Spiders.MobyGames import MobyGamesSpider
from gensim.corpora import Dictionary
from WikiSpaCyCorpus import WikiSpacyCorpus
from gensim.models import LdaModel

data_manager = DataManager()
data_manager.crawl(source="Wikipedia")

# If dictionary was already created, load it
# Otherwise ensure that the variable is kept as None (as expected by Gensim)
path_dictionary = "Data/ID2Word"
dictionary = Dictionary.load(path_dictionary) if os.path.exists(path_dictionary) else None

# Note that the input attribute needs to be manually set
wiki = WikiSpacyCorpus("Data/Wikipedia.xml", article_min_tokens=200, dictionary=dictionary)
setattr(wiki, "input", wiki.fname)

if not os.path.exists(path_dictionary):
    wiki.dictionary.filter_extremes(no_below=20, no_above=0.1)
    dictionary = wiki.dictionary
    dictionary.save(path_dictionary)

if os.path.exists("Data/BOW"):
    with open("Data/BOW", "rb") as file:
        bow = pickle.load(file)
else:
    bow = [dictionary.doc2bow(game) for game in wiki.get_texts()]

    with open("Data/BOW", "wb") as file:
        pickle.dump(bow, file)

path_lda = "Data/LDA/LDA"
if os.path.exists(path_lda):
    lda = LdaModel.load(path_lda)
else:
    os.makedirs(path_lda[:-4], exist_ok=True)
    lda = LdaModel(corpus=bow, id2word=dictionary)
    lda.save(path_lda)
