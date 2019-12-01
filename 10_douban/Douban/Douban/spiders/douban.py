# -*- coding: utf-8 -*-
import json
import time
import requests
from ..filmtype import *
from ..items import *


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/']
    print('电影类型：剧情|喜剧|动作|爱情|科幻|动画|悬疑|惊悚|恐怖|纪录片|短片|情色|同性|音乐|歌舞|家庭|儿童|传记|历史|战争|犯罪|西部|奇幻|冒险|灾难|武侠|古装|运动|黑色电影')
    type_name = input('请选择电影类型：')
    # 获取对应type值
    type = filmtype[type_name]

    url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'

    def get_count(self, type):
        '''
        获取该电影类型一共多少电影
        :param type_name:
        :param type:
        :return:
        '''
        url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90'
        html = requests.get(
            url=url.format(type),
            headers={'User-Agent': 'Mozilla/5.0'}
        ).json()
        return html['total']

    def start_requests(self):
        count = int(self.get_count(self.type)) + 1
        for start in range(0, count, 20):
            url = self.url.format(self.type, start)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        item = DoubanItem()
        html = json.loads(response.text)
        for film in html:
            item['_id'] = time.time()
            item['title'] = film['title']
            item['star'] = film['actors']
            item['score'] = film['score']
            item['time'] = film['release_date']
            yield item

