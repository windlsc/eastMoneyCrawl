# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt

class pipelines2excel(object):
	
	def open_spider(self, spider):
			self.wb = xlwt.work
			self.db = self.client[self.mongo_db]
	
	def close_spider(self, spider):
			self.client.close()
	
	def process_item(self, item, spider):
			if isinstance(item, company_info):
				self.db['company_info'].update_one(dict(item), {'$set':dict(item)}, upsert=True)
			elif isinstance(item, fund_info):
				self.db['fund_info'].update_one(dict(item), {'$set':dict(item)}, upsert=True)
			elif isinstance(item, fund_values):
				values_d = dict(item)
				fund_id = values_d['fund_id']
				del values_d['fund_id']
				self.db[fund_id].update_one(values_d, {'$set':values_d}, upsert=True)
			return item
