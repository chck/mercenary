# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MercenaryItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    locality = scrapy.Field()
    url = scrapy.Field()
    cp = scrapy.Field()
    quantity = scrapy.Field()
    price = scrapy.Field()
    careful_quantities = scrapy.Field()
    raw = scrapy.Field()
