# -*- coding: utf-8 -*-
import random
import time

import scrapy
from ..items import *

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    # start_urls = ['http://maoyan.com/']  # 注释初始地址

    # 重写start_requests()方法
    def start_requests(self):
        item = MaoyanItem()
        for offset in range(5):
            url = 'https://maoyan.com/board/6?offset={}'.format(offset)
            yield scrapy.Request(
                url = url,
                # 不同解析函数之间传递数据
                meta = {'item': item},
                callback = self.parse
            )

    def parse(self, response):
        item = response.meta['item']
        r_list = response.xpath('//dl[@class="board-wrapper"]/dd')
        for r in r_list:
            item['_id'] = time.time()
            item['name'] = r.xpath('.//p[@class="name"]/a/text()').get()
            item['star'] = r.xpath('.//p[@class="star"]/text()').get()
            item['time'] = r.xpath('.//p[@class="releasetime"]/text()').get()
            yield item
