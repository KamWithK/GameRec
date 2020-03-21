#!/usr/bin/env python
# coding: utf-8

import scrapy, os, requests

from scrapy.spiders import CrawlSpider
from os.path import splitext
from shutil import copyfileobj

class MobyGamesSpider(CrawlSpider):
    def __init__(self, game_titles):
        # Use the dictionary of URL as keys as pages to start scraping
        self.titles = game_titles
        self.start_urls = list(self.titles.keys())

    # Parse the search URL through each function
    # To allow the game title to be found through its URL
    def parse(self, response):
        image_response = response.css("div.searchTitle > a::attr(href)").get()
        if image_response != None:
            yield scrapy.Request(image_response, callback=self.parse_game, cb_kwargs={"search_url": response.request.url})

    def parse_game(self, response, search_url):
        image_response = response.css("div#coreGameCover > a::attr(href)").get()
        if image_response != None:
            yield scrapy.Request(image_response, callback=self.parse_image, cb_kwargs={"search_url": search_url})

    def parse_image(self, response, search_url):
        partial_url = response.css("img.img-responsive::attr(src)").get()
        download_url = "https://www.mobygames.com" + partial_url
        image_path = "Data/Images/" + self.titles[search_url] + splitext(partial_url)[1]

        # Download image when page loads without problems
        # Bypass errors
        request = requests.get(download_url, stream=True)
        try:
            if request.status_code == 200:
                os.makedirs("Data/Images", exist_ok=True)
                with open(image_path, "wb") as image:
                    request.raw.decode_content = True
                    copyfileobj(request.raw, image)
        except:
            pass

        yield None