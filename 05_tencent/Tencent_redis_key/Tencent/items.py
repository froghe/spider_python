# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 岗位名称
    recruitPostName = scrapy.Field()
    # 工作要求
    requirement = scrapy.Field()
    # 工作职责
    responsibility = scrapy.Field()
    # 工作类别
    categoryName = scrapy.Field()
    # 工作地点
    locationName = scrapy.Field()
    # 发布时间
    lastUpdateTime = scrapy.Field()