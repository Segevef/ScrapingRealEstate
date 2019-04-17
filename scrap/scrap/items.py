# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


#  Zillow home listing item
class HomeListing(scrapy.Item):
    zid = scrapy.Field()
    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    pgapt = scrapy.Field()  # 'status, example "for sale"'
    sgapt = scrapy.Field()  # 'who sales, broker?'
    link = scrapy.Field()
    list_price = scrapy.Field()
    beds = scrapy.Field()
    baths = scrapy.Field()
    sq_feet = scrapy.Field()

