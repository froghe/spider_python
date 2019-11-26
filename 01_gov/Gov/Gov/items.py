# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GovItem(scrapy.Item):
    # define the fields for your item here like:
    # 定义最终需要抓取的数据
    # 代码 + 名称
    code = scrapy.Field()
    name = scrapy.Field()
