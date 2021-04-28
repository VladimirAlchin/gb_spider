# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookLabirintItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    rate = scrapy.Field()
    authors = scrapy.Field()
    cost_old = scrapy.Field()
    cost_new = scrapy.Field()
    currency = scrapy.Field()
    data_cost = scrapy.Field()

    # pass
