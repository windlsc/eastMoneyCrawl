# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

#import eastMoneyCrawl
#from eastMoneyCrawl import pipelines
from eastMoneyCrawl.items import fundCompanyItem
from scrapy.shell import inspect_response

class fundCompanyInfoSpider(CrawlSpider):
	name = 'fundCompanyInfoSpider'
	allowed_domains = ['eastmoney.com']
	start_urls = ['http://fund.eastmoney.com/Company/default.html']
	#start_urls = ['http://fund.eastmoney.com/Company/80163340.html']
	custom_settings = {
			'ITEM_PIPELINES':{'eastMoneyCrawl.pipelines.EastmoneycrawlPipeline':300,}
	}
	#rules = (
	#		Rule(LinkExtractor(allow=(r'/Company/\d{8}\.html$')), callback='parse_item', follow=False),
	#)
	
	def parse(self, response):
		#link = LinkExtractor(allow=(r'/Company/\d{8}\.html$'))
		#links = link.extract_links(response)
		#if links:
		#		for link_one in links:
		#				print (link_one)
		parent_url = os.path.dirname(os.path.dirname(response.url))
		for href in response.xpath(r'//div[@class="sencond-block"]/a/@href').extract():
				full_url = parent_url + href
				print(full_url)
				yield scrapy.Request(full_url, callback=self.parse_item)
						
	def parse_item(self, response):
			#inspect_response(response, self)
			fund_company_name = response.xpath('.//div[@class="common-basic-info"]//p[@class="ttjj-panel-main-title"]/text()').extract()[0]
			fund_company_scale = response.xpath('.//div[@class="fund-info"]/ul/li[1]/label[@class="grey"]/text()').extract()[0]
			fund_company_funds_num = response.xpath('.//div[@class="fund-info"]/ul/li[2]/label[@class="grey"]/a/text()').extract()[0]
			fund_company_managers_num = response.xpath('.//div[@class="fund-info"]/ul/li[3]/label[@class="grey"]/a/text()').extract()[0]
			fund_company_rating = len(response.xpath('.//div[@class="fund-info"]/ul/li[@class="rating"]/label[@class="star grade iconfont"]').extract())
			fund_company_date = response.xpath('.//div[@class="fund-info"]/ul/li[@class="date"]/label[@class="grey"]/text()').extract()[0]
			fund_company_info = fundCompanyItem(fund_company_name = fund_company_name,
												fund_company_scale = fund_company_scale,
												fund_company_funds_num = fund_company_funds_num,
												fund_company_managers_num = fund_company_managers_num,
												fund_company_rating = fund_company_rating,
												fund_company_date = fund_company_date,
												)
			yield fund_company_info
			