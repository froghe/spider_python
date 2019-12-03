# -*- coding: utf-8 -*-
import json
import os

import scrapy
from urllib import parse
from ..items import *

class BaiduimageSpider(scrapy.Spider):
    name = 'baiduimage'
    allowed_domains = ['image.baidu.com']
    # start_urls = ['http://image.baidu.com/']

    directory = 'F:\\04_gitProject\\11_baiduImage\\BaiduImage\\'
    if not os.path.exists(directory):
        os.makedirs(directory)

    url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&' \
          'fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8' \
          '&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={}&' \
          's=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={}&rn=30&gsm=&1575268638962='
    inputtext = input('请输入需要下载的图片：')
    word = parse.quote(inputtext)

    def start_requests(self):
        for pn in range(0, 151, 30):
            url = self.url.format(self.word, self.word, pn)
            yield scrapy.Request(
                url = url,
                callback = self.parse
            )

    def parse(self, response):
        html = json.loads(response.text)['data']
        item = BaiduimageItem()
        for image in html:
            item['img_title'] = image['fromPageTitleEnc']
            item['img_url'] = image['middleURL']
            yield item



