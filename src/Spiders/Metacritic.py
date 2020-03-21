#!/usr/bin/env python
# coding: utf-8

import scrapy

from scrapy.spiders import CrawlSpider, Rule

class MetacriticSpider(CrawlSpider):
    name = "metacritic"

    start_urls = ["https://www.metacritic.com/browse/games/release-date/available/pc/metascore"]

    # Returns a dictionary with URL and title
    def parse(self, response):
        # Exit when scrapping a non-intended page
        if not self.start_urls[0] in response.request.url:
            return
        
        all_css_selector = "div.product_title > a::attr(href)"
        next_css_selector = "span.next > a.action::attr(href)"

        # Parse every single listed game
        for url in response.css(all_css_selector).getall():
            yield response.follow(url, callback=self.parse_game)

        next_page = response.css(next_css_selector).get()

        # If a link to another page is present, assume it exists
        if next_page != None:
            print("Going to the next page")
            yield response.follow(next_page, callback=self.parse)

    def parse_game(self, response):
        title_css_selector = "div.product_title > a > h1::text"

        # Use the best summary available
        # To overcomes Metacritic's unpredictabilness
        summary = response.css(".data > span > span.blurb_expanded::text").get(default="").strip()
        if summary == "":
            summary = response.css(".product_summary > span.data > span::text").get(default="").strip()

            # Slip over entries without a summary
            if summary == "":
                print(response.request.url)
                return

        yield {
            "url": response.request.url,
            "game_title": response.css(title_css_selector).get().strip(),
            "summary": summary,
        }
