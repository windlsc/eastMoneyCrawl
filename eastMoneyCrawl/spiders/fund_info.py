# -*- coding: utf-8 -*-
import os
import scrapy
from lxml import etree
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

#import eastMoneyCrawl
#from eastMoneyCrawl import pipelines
from eastMoneyCrawl.items import fundCompanyItem
from scrapy.shell import inspect_response
#from gerapy_selenium import SeleniumRequest

class fund_info(CrawlSpider):
	name = 'fund_info'
	allowed_domains = ['eastmoney.com']
	start_urls = ['http://fund.eastmoney.com/Company/default.html']
	custom_settings = {
			'DOWNLOADER_MIDDLEWARES':{'eastMoneyCrawl.middlewares.seleniumMiddleware.seleniumMiddleware':545,}
			'ITEM_PIPELINES':{'eastMoneyCrawl.pipelines2mongo.pipelines2mongo':300,}
	}
	rules = (
			Rule(LinkExtractor(allow=(r'/Company/\d{8}\.html$')), call_back='parse_item'),
			#Rule(LinkExtractor(allow=(r'fund\.eastmoney\.com/\d{6}\.html')), )
			#Rule(LinkExtractor(allow=(r'fundf10\.eastmoney\.com/jjjz_\d{6}\.html')), call_back='parse_item')
	)
	
						
	def parse_item(self, response):
			#inspect_response(response, self)
			company_name = response.xpath('.//div[@class="common-basic-info"]//p[@class="ttjj-panel-main-title"]/text()').extract()[0]
			company_scale = response.xpath('.//div[@class="fund-info"]/ul/li[1]/label[@class="grey"]/text()').extract()[0]
			company_funds = response.xpath('.//div[@class="fund-info"]/ul/li[2]/label[@class="grey"]/a/text()').extract()[0]
			company_managers = response.xpath('.//div[@class="fund-info"]/ul/li[3]/label[@class="grey"]/a/text()').extract()[0]
			company_rating = len(response.xpath('.//div[@class="fund-info"]/ul/li[@class="rating"]/label[@class="star grade iconfont"]').extract())
			company_date = response.xpath('.//div[@class="fund-info"]/ul/li[@class="date"]/label[@class="grey"]/text()').extract()[0]
			company_info = company_info(company_name = company_name,
										company_scale = company_scale,
										company_funds = company_funds,
										company_managers = company_managers,
										company_rating = company_rating,
										company_date = company_date,
										)
			yield company_info
			#fund info
			for href in response.xpath(r'//td[@class=fund-name-code]/a[1]/@href').extract():
				request = scrapy.Request(href, callback='parse_fund_info')
				yield request
	
	def parse_fund_info(self, response):
			fund_name = response.xpath('.//div[@class="fundDetail-header"]//div/div/text()').extract()[0]
			fund_id = response.xpath('.//div[@class="fundDetail-header"]//div/div/span[2]/text()').extract()[0]
			fund_type = response.xpath('.//div[@class="infoOfFund"]//tbody/tr[1]/td[1]/a/text()').extract()[0]
			fund_scale = response.xpath('.//div[@class="infoOfFund"]//tbody/tr[1]/td[2]/text()').extract()[0]
			fund_manager = response.xpath('.//div[@class="infoOfFund"]//tbody/tr[1]/td[1]/a/text()').extract()[0]
			fund_foundation_date = response.xpath('.//div[@class="infoOfFund"]//tbody/tr[2]/td[1]/text()').extract()[0]
			fund_info = fund_info(fund_name = scrapy.Field()
								  fund_scale = fund_scale,
									fund_id = fund_id,
									fund_type = fund_type,
									fund_manager = fund_manager,
									fund_foundation_date = fund_foundation_date,
			)
			yield fund_info
			#fund_value
			value_url = 'http://fundf10.eastmoney.com/jjjz_'+fund_id+'.html'
			yield Request(value_url, callback=self.parse_fund_value)

	def parse_fund_value(self, response):
		#total_page = int(response.xpath(r'.//div[@class="pagebtns"]/label[last()-1]/text()').extract()[0])
		#cur_page = int(response.xpath(r'.//div[@class="pagebtns"]/label[@class="cur"]/text()').extract()[0])
		url = response.url
		source_l = response.body.split(' ')
		total_page = len(source_l)/2
		source_d = {source_l[i]:source_l[i+1] for i in range(0, len(source_l), 2)}
		for page, source in source_d.items():
			print('{0}/{1} for {2}'.format(page, total_page, url))
			html = etree.HTML(source)
			fund_id = re.search(r'.* \((\d{6})\)', html.xpath(r'.//div[@class="bs_jz"]/div/h4/a/text()')[0]).groups()[0]
			for tr in html.xpath(r'.//div[@id="jztable"]//tr'):
					fund_date = tr.xpath(r'./td[1]/text()').extract()[0]
					fund_value = tr.xpath(r'./td[2]/text()').extract()[0]
					fund_values = fund_values(fund_id = fund_id,
									  fund_date = fund_date,
									  fund_value = fund_value,
					)
					yield fund_values
		 


			