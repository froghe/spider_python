# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from .settings import *


class GovPipeline(object):
    def process_item(self, item, spider):
        print(item['code'], item['name'])
        return item


# 自定义管道文件 mysql
class GovMysqlPipeline(object):
    def open_spider(self, spider):
        self.db = pymysql.connect(
            host = MYSQL_HOST,
            user = MYSQL_USER,
            password = MYSQL_PWD,
            database = MYSQL_DB,
            charset = MYSQL_CHAR
        )
        self.cursor = self.db.cursor()
        # 先清空表中的数据
        del1 = 'delete from province'
        del2 = 'delete from city'
        del3 = 'delete from county'
        self.cursor.execute(del1)
        self.cursor.execute(del2)
        self.cursor.execute(del3)
        self.db.commit()

    def process_item(self, item, spider):
        ins1 = 'insert into province values (%s, %s)'
        ins2 = 'insert into city values (%s, %s, %s)'
        ins3 = 'insert into county values (%s, %s, %s)'
        code = item['code']
        name = item['name']
        # 省
        if code[-4:] == '0000':
            L = [name, code]
            self.cursor.execute(ins1, L)
            # 直辖市添加到市表
            if name in ['北京市', '天津市', '上海市', '重庆市']:
                L = [name, code, code]
                self.cursor.execute(ins2, L)
        # 市
        elif code[-2:] == '00':
            L = [name, code, (code[:2] + '0000')]
            self.cursor.execute(ins2, L)
        # 县/区
        else:
            # 直辖市中的区
            if code[:2] in ['11', '12', '31', '50']:
                L = [name, code, (code[:2] + '0000')]
                self.cursor.execute(ins3, L)
            else:
                L = [name, code, (code[:4] + '00')]
                self.cursor.execute(ins3, L)

        self.db.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

