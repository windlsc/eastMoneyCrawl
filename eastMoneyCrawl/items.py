# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class fundCompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	fund_company_name = scrapy.Field()
	fund_company_scale = scrapy.Field()
	fund_company_funds_num = scrapy.Field()
	fund_company_managers_num = scrapy.Field()
	fund_company_rating = scrapy.Field()
	fund_company_date = scrapy.Field()
	
	
	
