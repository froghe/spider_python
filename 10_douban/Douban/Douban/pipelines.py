# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class DoubanPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item


class DoubanMongoPipeline(object):
    def open_spider(self, spider):
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn['doubandb']
        self.myset = self.db['filmtab']

    def process_item(self, item, spider):
        self.myset.insert_one(item)
        return item

    def close_spider(self, spider):
        self.conn.close()
