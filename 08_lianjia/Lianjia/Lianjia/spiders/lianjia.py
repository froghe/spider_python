# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

from ..items import *

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['sz.lianjia.com']
    # start_urls = ['http://sz.lianjia.com/']

    def start_requests(self):
        for pg in range(1, 3):
            url = 'https://sz.lianjia.com/ershoufang/pg{}/'.format(pg)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        html = response.text
        bs = BeautifulSoup(html, 'lxml')
        # 找到所有的房源，只找直接子节点，加参数recursive=False
        li_list = bs.find_all('li', attrs={'class': 'clear LOGVIEWDATA LOGCLICKDATA'})
        item = LianjiaItem()
        # 遍历每个房源信息
        for li in li_list:
            # 小区名 + 地点 + 户型 + 平方 + 朝向 + 装修 + 楼层 + 建造时间 + 构造 + 总价 + 单价 + 其它
            item['name'] = li.select('div .positionInfo > a')[0].get_text().strip()  # div标签class值为pos..的子标签 a
            item['addr'] = li.select('div .positionInfo > a')[1].get_text()
            item['type'] = li.select('div .houseInfo')[0].get_text().split('|')[0].strip()
            item['square'] = li.select('div .houseInfo')[0].get_text().split('|')[1].strip()
            item['orientation'] = li.select('div .houseInfo')[0].get_text().split('|')[2].strip()
            item['finish'] = li.select('div .houseInfo')[0].get_text().split('|')[3].strip()
            item['floor'] = li.select('div .houseInfo')[0].get_text().split('|')[4].strip()
            item['time'] = li.select('div .houseInfo')[0].get_text().split('|')[5].strip()
            item['structure'] = li.select('div .houseInfo')[0].get_text().split('|')[6].strip()
            item['totalPrice'] = li.select('div .totalPrice')[0].get_text()
            item['unitPrice'] = li.select('div .unitPrice')[0].get_text()
            item['other'] = li.select('div .tag')[0].get_text()

            yield item
