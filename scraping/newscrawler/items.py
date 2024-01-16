# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Lien(scrapy.Item):
    url = scrapy.Field()

class UrlStock(scrapy.Item):
    title = scrapy.Field()
    developers = scrapy.Field()
    publisher = scrapy.Field()
    ig_review_average = scrapy.Field()
    ig_review_number = scrapy.Field()
    discounted = scrapy.Field()
    date_published = scrapy.Field()
    final_price = scrapy.Field()
    tags = scrapy.Field()
    genres = scrapy.Field()
    original_selling_platform = scrapy.Field()
    playable_platform = scrapy.Field()
    editions = scrapy.Field()
