import re

import requests
from bs4 import BeautifulSoup


class DoubanSpider(object):
	def __init__(self):
		self.url = 'https://movie.douban.com/chart'

	def get_html(self):
		'''
		获取电影类型
		:return:
		'''
		html = requests.get(url=self.url, headers={'User-Agent': 'Mozilla/5.0'}).text
		bs = BeautifulSoup(html, 'lxml')
		a_list = bs.select('div .types > span > a')
		item = {}
		for a in a_list:
			string = a.get('href')
			name = re.findall('name=(.*?)&', string)[0]
			type = re.findall('type=(.*?)&', string)[0]
			item[name] = type
		print(item)


	def run(self):
		self.get_html()

if __name__ == '__main__':
	spider = DoubanSpider()
	spider.run()