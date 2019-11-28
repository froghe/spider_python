# -*- coding: utf-8 -*-
import json
import math
from urllib import parse
from ..items import *
import requests
import scrapy


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    # start_urls = ['http://careers.tencent.com/']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1574903675372&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1574904000834&postId={}&language=zh-cn'
    word = input('请输入需要查询的岗位：')

    # 获取页数
    def get_pages(self, keyword):
        url = self.one_url.format(keyword, 1)
        html = requests.get(url=url).json()
        # 不能使用地板除，因为12和20 都是需要2页，但是地板除结果不一样
        return math.ceil(html['Data']['Count'] / 10)

    # 重写start_requests
    def start_requests(self):
        '''
        遍历每页
        :return:
        '''
        # 处理中文编码问题
        keyword = parse.quote(self.word)
        # 获取页数
        pages = self.get_pages(keyword)
        # 遍历每个页面
        for index in range(1, pages + 1):
            url = self.one_url.format(keyword, index)
            yield scrapy.Request(
                url = url,
                callback = self.get_detailsPage_link
            )

    def get_detailsPage_link(self, response):
        '''
        遍历每个招聘信息
        :param response:
        :return:
        '''
        html = json.loads(response.text)
        r_list = html['Data']['Posts']
        for r in r_list:
            postid = r['PostId']
            url = self.two_url.format(postid)
            yield scrapy.Request(
                url = url,
                callback = self.parse_details
            )

    def parse_details(self, response):
        '''
        抓取详细信息
        :param response:
        :return:
        '''
        item = TencentItem()
        html = json.loads(response.text)
        # 岗位名称
        item['recruitPostName'] = html['Data']['RecruitPostName']
        # 工作要求
        item['requirement'] = html['Data']['Requirement'].replace('\r', '').replace('\n', '')
        # 工作职责
        item['responsibility'] = html['Data']['Responsibility'].replace('\r', '').replace('\n', '')
        # 工作类别
        item['categoryName'] = html['Data']['CategoryName']
        # 工作地点
        item['locationName'] = html['Data']['LocationName']
        # 发布时间
        item['lastUpdateTime'] = html['Data']['LastUpdateTime']
        yield item
