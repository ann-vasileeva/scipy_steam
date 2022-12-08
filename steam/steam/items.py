# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    category = scrapy.Field()
    reviews_cnt = scrapy.Field()
    overview = scrapy.Field()
    release_date = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    available_platforms() = scrapy.Field()

