# -*- coding: utf-8 -*-
import re
from ..items import *


class GovSpider(scrapy.Spider):
    name = 'gov'
    allowed_domains = ['www.mca.gov.cn']
    # start_urls = ['http://www.mca.gov.cn/']

    def start_requests(self):
        url = 'http://www.mca.gov.cn/article/sj/xzqh/2019/'
        yield scrapy.Request(
            url = url,
            callback = self.get_false_html
        )

    def get_false_html(self, response):
        '''
        获取假链接
        :param response:
        :return:
        '''
        html = response.text
        re_bds = r'class="artitlelist" href="(.*?)"'
        r_list = re.findall(re_bds, html, re.S)
        false_url = 'http://www.mca.gov.cn' + r_list[1]
        yield scrapy.Request(
            url = false_url,
            callback = self.get_real_html
        )

    def get_real_html(self, response):
        '''
        获取真链接
        :param response:
        :return:
        '''
        html = response.text
        re_bds = r'window.location.href="(.*?)"'
        real_link = re.findall(re_bds, html, re.S)[0]
        yield scrapy.Request(
            url = real_link,
            callback = self.parse
        )

    def parse(self, response):
        item = GovItem()
        xpath_bds = '//tr[@height="19"]'
        r_list = response.xpath(xpath_bds)
        for r in r_list:
            item['code'] = r.xpath("./td[2]/text()").get()
            item['name'] = r.xpath("./td[3]/text()").get()
            yield item
