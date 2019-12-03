# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class BaiduimagePipeline(object):
#     def process_item(self, item, spider):
#         return item
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class BaiduimagePipeline(ImagesPipeline):
    # 重写
    def get_media_requests(self, item, info):
        # 直接交给调度器入队列
        yield scrapy.Request(
            url = item['img_url'],
            meta = {'title': item['img_title']}
        )

    # 重写file_path()方法，解决 路径+文件名 问题
    def file_path(self, request, response=None, info=None):
        title = request.meta['title']
        filename = title + '.' + request.url.split('.')[-1]
        return filename