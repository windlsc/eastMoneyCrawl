# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class pipelines2mongo(object):

	def __init__(self, mongo_uri, mongo_db):
			self.mongo_uri = mongo_uri
			self.mongo_db = mongo_db
			
	@classmethod
	def from_crawler(cls, crawler):
			return cls(
					mongo_uri = crawler.settings.get('MONGO_URI'),
					mongo_db = crawler.settings.get('MONGO_DB', 'items')
			)
	
	def open_spider(self, spider):
			self.client = pymongo.MongoClient(self.mongo_uri)
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
