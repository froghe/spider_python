import json
import math
import time
from multiprocessing import Process
from queue import Queue
from threading import Thread, Lock
from urllib import parse
import requests
from fake_useragent import UserAgent

class TCSpider_thread(object):
	def __init__(self):
		self.one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1575342458572&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
		self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1575342585161&postId={}&language=zh-cn'
		self.i = 0
		self.ua = UserAgent()
		# 创建一个队列
		self.q = Queue()
		self.lock = Lock()

	def get_html(self, url):
		headers = {'User-Agent': self.ua.random}
		return requests.get(url=url, headers=headers).json()

	def parse_one_html(self):
		while True:
			if not self.q.empty():  # 队列不为空
				url = self.q.get()
				html = self.get_html(url)
				p_list = html['Data']['Posts']
				for p in p_list:
					postid = p['PostId']
					self.parse_two_html(self.two_url.format(postid))
			else:
				break

	def parse_two_html(self, url):
		item = {}
		html = self.get_html(url)['Data']
		# 岗位名称 + 地点 + 类别 + 工作职责 + 工作要求 + 发布时间
		item['name'] = html['RecruitPostName']
		item['address'] = html['LocationName']
		item['type'] = html['CategoryName']
		item['responsibility'] = html['Responsibility'].replace('\r\n', '').replace('\n', '')
		item['require'] = html['Requirement'].replace('\r\n', '').replace('\n', '')
		item['time'] = html['LastUpdateTime']
		print(item)

		# 在线程中创建item不需要加锁
		with open('tencent.json', 'a') as f:
			json.dump(item, f, ensure_ascii=False)

		self.i += 1

	def get_count(self, url):
		count = self.get_html(url)['Data']['Count']
		page = math.ceil(int(count) / 10) + 1
		return page

	def run(self):
		word = input('请输入搜索岗位：')
		keyword = parse.quote(word)
		page = self.get_count(self.one_url.format(keyword, 1))
		for pn in range(1, page):
			url = self.one_url.format(keyword, pn)
			# url入队列
			self.q.put(url)

		t_list = []
		for i in range(5):
			t = Thread(target=self.parse_one_html)  # 创建多线程 进程改为Process
			t_list.append(t)
			t.start()  # 启动

		for t in t_list:
			t.join()  # 回收

		print('一共%d条数据' % self.i)

if __name__ == '__main__':
	start = time.time()
	spider = TCSpider_thread()
	spider.run()
	end = time.time()
	print('执行时间：%.2f' % (end-start))
