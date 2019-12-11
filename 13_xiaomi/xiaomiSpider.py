import csv
import random
import time
from queue import Queue
from threading import Thread, Lock
import requests
from fake_useragent import UserAgent
from lxml import etree


class XiaoMiSpider(object):
	def __init__(self):
		self.one_url = 'http://app.mi.com/'
		self.two_url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId={}&pageSize=30'
		self.ua = UserAgent()
		self.i = 0
		# 创建空队列
		self.q = Queue()
		self.f = open('xiaomi.csv', 'a', encoding='utf-8', newline='')
		self.writer = csv.writer(self.f)
		# 创建线程锁
		self.lock = Lock()

	def get_html(self, url):
		headers = {'User-Agent': self.ua.random}
		return requests.get(url=url, headers=headers, timeout=5)

	def get_app_type(self):
		'''
		获取所有应用分类
		:return:
		'''
		html = self.get_html(self.one_url).text
		parse_html = etree.HTML(html)
		a_list = parse_html.xpath('//div[@class="sidebar"]/div[2]/ul/li/a')
		# 16个分类
		for a in a_list:
			name = a.xpath('./text()')[0]
			code = a.xpath('./@href')[0].split('/')[-1]
			print('-'*30 + name + '-'*30)
			self.get_app_html(code)

	def get_count(self, code):
		'''
		获取分类有多少个应用
		:param code:
		:return: 应用个数
		'''
		url = self.two_url.format(0, code)
		count = self.get_html(url).json()['count']
		# print('-' * 30 + str(count) + '-' * 30)
		# page = math.ceil(count / 30)
		page = count // 30 + 1
		return page

	def get_app_html(self, code):
		'''
		获取所有应用页面
		:param code:
		:return:
		'''
		page = self.get_count(code)
		for pg in range(2):
			url = self.two_url.format(pg, code)
			# self.parse_html(url)
			# url入队列
			self.q.put(url)
			print(url)
			# time.sleep(random.uniform(1, 2))

	def parse_html(self):
		'''
		解析应用
		:param url:
		:return:
		'''
		while True:
			app_list = []
			if not self.q.empty():  # 如果队列不为空
				url = self.q.get()
				html = self.get_html(url).json()
				data = html['data']
				for dic in data:
					# name = [dic['displayName'] if dic else None][0]
					name = dic.get('displayName', None)
					print(name)
					self.i += 1
					app_list.append(name)
				self.lock.acquire()
				self.writer.writerow(app_list)
				self.lock.release()
				time.sleep(1)
			else:
				break

	def run(self):
		# url入队列
		self.get_app_type()

		t_list = []
		for i in range(15):
			t = Thread(target=self.parse_html)
			t_list.append(t)
			t.start()

		for t in t_list:
			t.join()

		print('一共%d个应用' % self.i)
		self.f.close()

if __name__ == '__main__':
	start = time.time()
	spider = XiaoMiSpider()
	spider.run()
	end = time.time()
	print('执行时间：%.2f' % (end-start))