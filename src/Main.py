#!/usr/bin/env python
# coding: utf-8

from scrapy.crawler import CrawlerProcess
from Spiders.Wikipedia import Spider

# Scrape Metacritic
process = CrawlerProcess(settings={
    "FEED_FORMAT": "json",
    "FEED_URI": "Data/Games.json",
    "COOKIES_ENABLED": "False",
    "LOG_LEVEL": "WARNING",
})

process.crawl(Spider)
process.start()