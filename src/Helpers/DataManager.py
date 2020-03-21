#!/usr/bin/env python
# coding: utf-8
import os, json

from twisted.internet import defer
from scrapy.crawler import CrawlerProcess
from Spiders.Wikipedia import WikipediaSpider
from Spiders.Metacritic import MetacriticSpider
from Spiders.MobyGames import MobyGamesSpider

class DataManager():
    def __init__(self):
        self.process = CrawlerProcess(settings={
            "FEED_FORMAT": "json",
            "FEED_URI": "Data/Data.json",
            "COOKIES_ENABLED": "False",
            "LOG_LEVEL": "WARNING",
        })

        # Avoid errors due to non-existant folders and pre-existant data files
        os.makedirs("Data/Images", exist_ok=True)
        if os.path.isfile("Data/Data.json"):
            os.remove("Data/Data.json")

    def get_game_titles(self):
        # Load json file
        with open("Data/Data.json") as titles:
            data = json.load(titles)

        # Iterates through the json file and extracts game titles
        return [line["game_title"] for line in data]

    def crawl(self, source="Wikipedia"):
        @defer.inlineCallbacks
        def crawl():
            if source == "Wikipedia":
                yield self.process.crawl(WikipediaSpider)
            elif source == "Metacritic":
                yield self.process.crawl(MetacriticSpider)
            else:
                pass
            yield self.process.crawl(MobyGamesSpider, self.get_game_titles())
            
        crawl()
        self.process.start()
