# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # 名称 + 主演 + 上演时间
    _id = scrapy.Field()  # 保存mongo数据库需要加上这个
    name = scrapy.Field()
    star = scrapy.Field()
    time = scrapy.Field()