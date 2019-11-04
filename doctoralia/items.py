# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Doctor(scrapy.Item):
    name = scrapy.Field()
    city = scrapy.Field()
    proficiency = scrapy.Field()
    specialty = scrapy.Field()
    estate = scrapy.Field()
    phone = scrapy.Field()
    score = scrapy.Field()
    address = scrapy.Field() 
    url = scrapy.Field()
