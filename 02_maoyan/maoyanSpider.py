import json
import random
import time
import requests
from fake_useragent import UserAgent
from lxml import etree


class MaoyanSpider(object):
	def __init__(self):
		self.url = 'https://maoyan.com/board/6?offset={}'
		self.ua = UserAgent()
		self.i = 0

	def get_html(self, url):
		'''
		请求响应
		:param url:
		:return:
		'''
		headers = {'User-Agent': self.ua.random}
		return requests.get(url=url, headers=headers).text

	def parse_html(self, url):
		'''
		xpath解析响应信息
		:param url:
		:return:
		'''
		html = self.get_html(url)
		xpath_html = etree.HTML(html)
		r_list = xpath_html.xpath('//dl[@class="board-wrapper"]/dd')
		item = {}
		for r in r_list:
			item['name'] = r.xpath('.//p[@class="name"]/a/text()')[0]
			item['star'] = r.xpath('.//p[@class="star"]/text()')[0]
			item['time'] = r.xpath('.//p[@class="releasetime"]/text()')[0]
			print(item)
			self.save_json(item)
			self.i += 1

	def save_json(self, item):
		'''
		保存为json文件
		:return:
		'''
		with open('maoyan.json', 'a') as f:
			json.dump(item, f, ensure_ascii=False)

	def run(self):
		for offset in range(5):
			url = self.url.format(offset)
			self.parse_html(url)
			time.sleep(random.uniform(1, 2))  # 爬取一个页面后休眠
		print('一共%d条数据' % self.i)


if __name__ == '__main__':
	start = time.time()
	spider = MaoyanSpider()
	spider.run()
	end = time.time()
	print('执行时间：%.2f' % (end - start))
