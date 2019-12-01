# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from .settings import *


class LianjiaPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item

class LianjiaMysqlPipeline(object):
    def open_spider(self, spider):
        self.db = pymysql.connect(
            host = MYSQL_HOST,
            user = MYSQL_USER,
            password = MYSQL_PWD,
            database = MYSQL_DB,
            charset = MYSQL_CHAR,
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        L = [
            item['name'],
            item['addr'],
            item['type'],
            item['square'],
            item['orientation'],
            item['finish'],
            item['floor'],
            item['time'],
            item['structure'],
            item['totalPrice'],
            item['unitPrice'],
            item['other'],
        ]
        ins = 'insert into linjiatab values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.cursor.execute(ins, L)
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
