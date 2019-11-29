import os
import random
import time
from urllib import parse
import requests
from bs4 import BeautifulSoup

class BaiduTieba(object):
	def __init__(self):
		self.url = 'http://tieba.baidu.com/f?kw={}&pn={}'
		self.i = 0

	def get_html(self, url):
		headers = {'User-Agent': 'Mozilla/5.0'}
		return requests.get(url=url, headers=headers)

	def parse_html(self, url, directory):
		'''
		解析贴吧，获取每个帖子详情的链接
		:param url:
		:return:
		'''
		html = self.get_html(url).text
		soup = BeautifulSoup(html, 'lxml')
		a_list = soup.find_all(
			'a', attrs={'class': 'j_th_tit'}
		)
		for a in a_list:
			url = 'http://tieba.baidu.com' + a.get('href')
			self.get_details_page(url, directory)
			time.sleep(random.uniform(1, 2))  # 每下载一个贴子的照片，休眠

	def get_details_page(self, url, directory):
		'''
		从每个帖子中获取图片
		:param url:
		:return:
		'''
		html = self.get_html(url).text
		soup = BeautifulSoup(html, 'lxml')
		img_list = soup.find_all(
			'img', attrs={'changedsize': 'true'}
		)
		for img in img_list:
			self.save_image(img.get('src'), directory)

	def save_image(self, img, directory):
		'''
		保存图片
		:param img:
		:return:
		'''
		html = self.get_html(img).content
		filename = directory + img.split('/')[-1]
		with open(filename, 'wb') as f:
			f.write(html)
			self.i += 1
			print('{} 下载完成'.format(filename))

	def run(self):
		word = input('请输入贴吧名：')
		directory = '.\\{}\\'.format(word)
		if not os.path.exists(directory):
			os.makedirs(directory)

		kw = parse.quote(word)
		for pn in range(0, 51, 50):
			url = self.url.format(kw, pn)
			self.parse_html(url, directory)
		print('一共%d张图片' % self.i)

if __name__ == '__main__':
	start = time.time()
	spider = BaiduTieba()
	spider.run()
	end = time.time()
	print('执行时间%.2f' % (end-start))
