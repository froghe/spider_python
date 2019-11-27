import random
import re
import time
import pymysql
import requests
from fake_useragent import UserAgent
from lxml import etree
from hashlib import md5


class FilmSpider(object):
	def __init__(self):
		self.url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
		self.ua = UserAgent()
		self.i = 0
		self.proxies = {
			'http': 'http://127.0.0.1:8888',
			'https': 'https://127.0.0.1:8888'
		}
		self.db = pymysql.connect('localhost', 'root', '123456', 'filmskydb', charset='utf8')
		self.cursor = self.db.cursor()

	def get_html(self, url):
		'''
		请求响应
		:param url:
		:return:
		'''
		headers = {'User-Agent': self.ua.random}
		return requests.get(
			url=url,
			headers=headers,
			proxies=self.proxies,
			verify=False
		).content.decode('gb2312', 'ignore')

	def get_link(self, url):
		'''
		获取每部电影详细页面的链接
		:param url:
		:return:
		'''
		html = self.get_html(url)
		parse_html = etree.HTML(html)
		xpath_bds = '//div[@class="co_content8"]/ul//a/@href'
		l_list = parse_html.xpath(xpath_bds)
		for l in l_list:
			link = 'https://www.dytt8.net' + l
			self.parse_html(link)
			time.sleep(random.uniform(1,2))

	def parse_html(self, link):
		'''
		抓取页面电影信息，并存入数据库
		:param link:
		:return:
		'''
		html = self.get_html(link)
		re_name = '<h1><font color=#07519a>.*?《(.*?)》'
		re_load = 'bgcolor="#fdfddf"><a href="(.*?)"'
		name = re.findall(re_name, html, re.S)
		name = [name[0] if name else None][0]
		print(name)
		load_link = re.findall(re_load, html, re.S)
		load_link = [load_link[0] if load_link else None][0]
		print(load_link)
		if load_link is None:
			return
		result, md5_string = self.check_exists(load_link)
		if result:
			return
		else:
			ins1 = 'insert into filmtab values (%s, %s)'
			ins2 = 'insert into request_finger values (%s)'
			self.cursor.execute(ins1, [name, load_link])
			self.cursor.execute(ins2, [md5_string])
			self.db.commit()
			print(name, load_link)
			self.i += 1

	def check_exists(self, load_link):
		'''
		检查电影是否已经抓取过
		:param load_link:
		:return:
		'''
		md5_string = self.md5_string(load_link)
		sql = 'select * from request_finger where finger = %s'
		result = self.cursor.execute(sql, [md5_string])
		return result, md5_string

	def md5_string(self, load_link):
		'''
		md5加密
		:param load_link:
		:return:
		'''
		s = md5()
		s.update(load_link.encode())
		return s.hexdigest()

	def run(self):
		for pn in range(1, 3):
			url = self.url.format(pn)
			self.get_link(url)
		print('爬取完成，一共%d条数据' % self.i)


if __name__ == '__main__':
	start = time.time()
	spider = FilmSpider()
	spider.run()
	end = time.time()
	print('执行时间：%.2f' %(end - start))
