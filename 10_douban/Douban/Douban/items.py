# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # id + 电影名称 + 主演 + 评分 + 上映时间
    _id = scrapy.Field()  # 保存mongo数据库需要加上这个
    title = scrapy.Field()
    star = scrapy.Field()
    score = scrapy.Field()
    time = scrapy.Field()
