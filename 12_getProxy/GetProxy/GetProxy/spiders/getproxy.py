# -*- coding: utf-8 -*-
import requests
import scrapy
from bs4 import BeautifulSoup
from ..items import *


class GetproxySpider(scrapy.Spider):
    name = 'getproxy'
    allowed_domains = ['www.baidu.com']
    # start_urls = ['http://www.baidu.com/']
    url = 'https://www.xicidaili.com/nn/{}'

    def start_requests(self):
        for pn in range(1, 3001):
            url = self.url.format(pn)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        html = response.text
        bs = BeautifulSoup(html, 'lxml')
        tr_list = bs.find_all('tr', attrs={'class': 'odd'})
        item = GetproxyItem()
        for tr in tr_list:
            item['ip'] = tr.select('td')[1].get_text()
            item['port'] = tr.select('td')[2].get_text()
            if self.test_proxy(item['ip'], item['port']):
                yield item

    def test_proxy(self, ip, port):
        proxies = {
            'http': 'http://{}:{}'.format(ip, port),
            'https': 'https://{}:{}'.format(ip, port)
        }
        url = 'http://www.baidu.com'
        try:
            res = requests.get(url=url, proxies=proxies, timeout=5)
            if res.status_code == 200:
                return True
        except Exception as e:
            return False
