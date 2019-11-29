import os
import random
import re
import time

import requests
from fake_useragent import UserAgent


class SoImage(object):
	def __init__(self):
		self.url = 'https://image.so.com/zjl?ch=beauty&t1={}&sn={}&listtype=new&temp=1'
		self.i = 0
		self.ua = UserAgent()

	def parse_html(self, t, url):
		'''
		遍历每组图片信息
		:param url:
		:return:
		'''
		headers = {'User-Agent': self.ua.random}
		html = requests.get(url=url, headers=headers).json()
		image_list = html['list']
		for image in image_list:
			# 图片张数 + 标题 + 每组图片链接
			count = int(image['grpcnt'])
			title = image['title']
			link = image['purl']
			self.group_image(count, link, title, t)

	def get_image(self, url):
		'''
		获取具体的每张照片的链接
		:param url:
		:return:
		'''
		headers = {'User-Agent': self.ua.random}
		html = requests.get(url=url, headers=headers).text
		re_bds = 'alt="" src="(.*?)"'
		return re.findall(re_bds, html, re.S)[0]

	def group_image(self, count, link, title, t):
		'''
		遍历每组图片，并保存
		:return:
		'''
		directory = '.\\image\\{}\\{}\\'.format(t, title)
		if not os.path.exists(directory):
			os.makedirs(directory)

		for pn in range(1, count + 1):
			if pn == 1:
				image = self.get_image(link)
			else:
				image = self.get_image(link[:-4] + '_%d' % pn + '.htm')
			self.save_image(image, pn, directory)
			self.i += 1
		time.sleep(random.uniform(1, 2))

	def save_image(self, image, pn, directory):
		'''
		保存图片
		:param image:
		:param title:
		:param i:
		:return:
		'''
		headers = {'User-Agent': self.ua.random}
		html = requests.get(url=image, headers=headers).content
		filename = directory + '{}.jpg'.format(pn)
		with open(filename, 'wb') as f:
			f.write(html)
			print('%s，保存成功' % filename)

	def run(self):
		# 遍历请求地址，每次请求30组图片
		print('cosplay、婚纱、明星、粉嫩、萌女、街拍、车模')
		while True:
			t = input('请输入需要爬取的类型：')
			if t == 'cosplay':
				code = 598
			elif t == '婚纱':
				code = 596
			elif t == '明星':
				code = 599
			elif t == '粉嫩':
				code = 625
			elif t == '萌女':
				code = 595
			elif t == '街拍':
				code = 603
			elif t == '车模':
				code = 600
			else:
				print('您的输入有误，请重新输入：\n')
				continue
			for sn in range(0, 61, 30):
				url = self.url.format(code, sn)
				self.parse_html(t, url)
			break
		print('一共%d张图片' % self.i)


if __name__ == '__main__':
	start = time.time()
	spider = SoImage()
	spider.run()
	end = time.time()
	print('执行时间：%.2f' % (end - start))
