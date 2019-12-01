# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # 小区名 + 地点 + 户型 + 平方 + 朝向 + 装修 + 楼层 + 建造时间 + 构造 + 总价 + 单价 + 其它
    name = scrapy.Field()
    addr = scrapy.Field()
    type = scrapy.Field()
    square = scrapy.Field()
    orientation = scrapy.Field()
    finish = scrapy.Field()
    floor = scrapy.Field()
    time = scrapy.Field()
    structure = scrapy.Field()
    totalPrice = scrapy.Field()
    unitPrice = scrapy.Field()
    other = scrapy.Field()