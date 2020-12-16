# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class company_info(scrapy.Item):
	company_name = scrapy.Field()
	company_scale = scrapy.Field()
	company_funds = scrapy.Field()
	company_managers = scrapy.Field()
	company_rating = scrapy.Field()
	company_date = scrapy.Field()


class fund_info(scrapy.Item):
	fund_name = scrapy.Field()
	fund_scale = scrapy.Field()
	fund_id = scrapy.Field()
	fund_type = scrapy.Field()
	fund_manager = scrapy.Field()
	fund_foundation_date = scrapy.Field()


class fund_values(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	fund_id = scrapy.Field()
	fund_date = scrapy.Field()
	fund_value = scrapy.Field()
	
	
	
