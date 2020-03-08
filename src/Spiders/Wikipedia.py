#!/usr/bin/env python
# coding: utf-8

import scrapy

from scrapy.spiders import CrawlSpider, Rule

class WikipediaSpider(CrawlSpider):
    name = "wikipedia"

    start_urls = ["https://en.wikipedia.org/wiki/List_of_PC_games"]

    # Returns a dictionary with URL and title
    def parse(self, response):
        pages_css_selector = "div.toc > div > ul > li > a::attr(href)"

        # Parse every single listed page of games
        # Skip the first though as first page otherwise loads twice
        for url in response.css(pages_css_selector).getall()[1:]:
            yield response.follow(url, callback=self.parse_games)

    def parse_games(self, response):
        # Get URLs and game titles
        urls_css_selector = "td > i > a::attr(href)"
        titles_css_selector = "td > i > a::text"

        # Automatically skips over any entries without a Wikipedia page/title
        for (url, title) in zip(response.css(urls_css_selector).getall(), response.css(titles_css_selector).getall()):
            yield {
                "wiki_title": url[6:],
                "game_title": title,
            }
