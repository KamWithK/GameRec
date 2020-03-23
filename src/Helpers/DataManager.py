#!/usr/bin/env python
# coding: utf-8
import os, json

from glob import glob
from twisted.internet import defer
from scrapy.crawler import CrawlerProcess
from Spiders.Wikipedia import WikipediaSpider
from Spiders.Metacritic import MetacriticSpider
from Spiders.MobyGames import MobyGamesSpider
from urllib.parse import quote

class DataManager():
    def __init__(self, redownload=False):
        self.redownload = redownload
        self.process = CrawlerProcess(settings={
            "FEED_FORMAT": "json",
            "FEED_URI": "Data/Data.json",
            "COOKIES_ENABLED": "False",
            "LOG_LEVEL": "WARNING",
        })

        # Avoid errors due to non-existant folders and pre-existant data files
        os.makedirs("Data/Images", exist_ok=True)
        if redownload == True or not os.path.isfile("Data/Data.json"):
            if os.path.isfile("Data/Data.json"):
                os.remove("Data/Data.json")

    def get_game_data(self):
        # Load json file
        with open("Data/Data.json") as titles:
            data = json.load(titles)

        # Create search a URL to game title dictionary
        return {"https://www.mobygames.com/search/quick?q=" + quote(line["game_title"]): line["game_title"] for line in data}

    def crawl(self, source="Wikipedia"):
        @defer.inlineCallbacks
        def crawl():
            # Assume images folder hasn't been manually deleted mid run
            game_list_present, images = os.path.isfile("Data/Data.json"), os.listdir("Data/Images/")

            if self.redownload or game_list_present == False:
                if source == "Wikipedia":
                    yield self.process.crawl(WikipediaSpider)
                elif source == "Metacritic":
                    yield self.process.crawl(MetacriticSpider)

            # Only scrape images for empty images directory or explicit command
            if self.redownload or not images:
                missing_images = {url: title for url, title in self.get_game_data().items() if not glob("Data/Images/" + title + ".*")}
                yield self.process.crawl(MobyGamesSpider, missing_images)
            
        crawl()
        self.process.start()
