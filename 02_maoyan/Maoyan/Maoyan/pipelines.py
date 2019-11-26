# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class MaoyanPipeline(object):
    def process_item(self, item, spider):
        print(item)
        # print(item['name'], item['star'], item['time'])
        return item


# 自定义管道文件，保存到mongo数据库
class MaoyanMongoPipeline(object):
    def open_spider(self, spider):
        self.conn = pymongo.MongoClient('localhost', 27017)  # 连接数据库
        self.db = self.conn['maoyandb']  # 创建库
        self.myset = self.db['filmtable']  #创建集合（表）

    def process_item(self, item, spider):
        self.myset.insert_one(item)
        return item

    def close_spider(self, spider):
        pass
