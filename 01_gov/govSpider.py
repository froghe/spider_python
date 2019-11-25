import csv
import re
import time
from hashlib import md5
import pymysql
import requests
from fake_useragent import UserAgent
from lxml import etree


class GovSpider(object):
	def __init__(self):
		self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2019/'
		self.ua = UserAgent()
		# 统计数据
		self.i = 0

	def mysql_connect(self):
		'''
		数据库连接
		:return:
		'''
		self.db = pymysql.connect('localhost', 'root', '123456', 'govdb', charset='utf8')
		self.cursor = self.db.cursor()
		# 创建3个列表，为executemany()使用
		self.province = []
		self.city = []
		self.county = []

	def get_html(self, url):
		'''
		向请求地址发送请求，得到响应信息字符串
		:param url: 请求地址
		:return: 响应信息字符串
		'''
		headers = {'User-Agent': self.ua.random}
		html = requests.get(url=url, headers=headers).text
		return html

	def re_select(self, re_bds, html):
		'''
		正则匹配字符
		:param re_bds: 正则表达式
		:param html: 响应信息字符串
		:return: 正则匹配的列表数据
		'''
		return re.findall(re_bds, html, re.S)

	def get_false_link(self):
		'''
		获取最新行政区划代码链接（假链接）
		:return: 假链接
		'''
		html = self.get_html(self.url)
		re_bds = r'class="artitlelist" href="(.*?)"'
		r_list = self.re_select(re_bds, html)
		false_url = 'http://www.mca.gov.cn' + r_list[1]
		return false_url

	def get_real_link(self):
		'''
		通过假链接发起请求，在响应的字符串信息中匹配真链接
		:return: 真链接
		'''
		false_url = self.get_false_link()
		html = self.get_html(false_url)
		re_bds = r'window.location.href="(.*?)"'
		real_url = self.re_select(re_bds, html)[0]
		return real_url

	def parse_html(self):
		'''
		解析响应信息，抓取数据
		:return: 数据列表
		'''
		real_url = self.get_real_link()
		html = self.get_html(real_url)
		xpath = '//tr[@height="19"]'
		parse_html = etree.HTML(html)
		r_list = parse_html.xpath(xpath)
		L = []
		for r in r_list:
			code = r.xpath("./td[2]/text()")[0]
			name = r.xpath("./td[3]/text()")[0]
			L.append((code, name))
			self.i += 1
		return L

	def save_csv(self):
		'''
		保存为csv文件
		:return:
		'''
		L = self.parse_html()
		with open('gov.csv', 'w', encoding='gbk', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(L)
		print('gov.csv文件保存成功')

	def md5_string(self, string):
		'''
		md5生成指纹函数
		:param string: 字符串
		:return: md5值
		'''
		s = md5()
		s.update(string.encode())
		md5_string = s.hexdigest()
		return md5_string

	def increment(self):
		'''
		增量爬取，检查当前数据库是否为最新的
		:return: 数据库查询结果
		'''
		url = self.get_real_link()
		incr = self.md5_string(url)
		sql = 'select * from version where url = %s'
		result = self.cursor.execute(sql, [incr])
		return result, incr

	def check_mysql(self):
		'''
		检查数据库是否需要更新
		:return:
		'''
		self.mysql_connect()  # 初始化数据库连接
		result, incr = self.increment()
		if result:
			print('网站未更新，无需抓取')
		else:
			dele = 'delete from version'
			self.cursor.execute(dele)
			ins = 'insert into version values (%s)'
			self.cursor.execute(ins, [incr])
			self.save_mysql()
			self.db.commit()  # 只有一个提交，保持数据一致
			print('保存到数据库成功')
		self.cursor.close()
		self.db.close()

	def save_mysql(self):
		'''
		把抓取到的数据存入数据库
		:return:
		'''
		L = self.parse_html()
		for i in L:
			code = i[0]
			name = i[1]
			# 省
			if code[-4:] == '0000':
				self.province.append([name, code])
				# 把直辖市加到city表
				if name in ['北京市', '天津市', '上海市', '重庆市']:
					self.city.append([name, code, code])
			# 市
			elif code[-2:] == '00':
				self.city.append([name, code, (code[:2] + '0000')])
			# 县/区
			else:
				if code[:2] in ['11', '12', '31', '50']:
					self.county.append([name, code, (code[:2] + '0000')])
				else:
					self.county.append([name, code, (code[:4] + '00')])
		self.insert_mysql()

	def insert_mysql(self):
		'''
		数据插入数据库
		:return:
		'''
		# 先清空表
		del1 = 'delete from province'
		del2 = 'delete from city'
		del3 = 'delete from county'
		self.cursor.execute(del1)
		self.cursor.execute(del2)
		self.cursor.execute(del3)
		# 插入数据
		ins1 = 'insert into province values (%s, %s)'
		ins2 = 'insert into city values (%s, %s, %s)'
		ins3 = 'insert into county values (%s, %s, %s)'
		self.cursor.executemany(ins1, self.province)
		self.cursor.executemany(ins2, self.city)
		self.cursor.executemany(ins3, self.city)

	def run(self):
		# self.save_csv()  # 保存为csv文件
		self.check_mysql()  # 保存到mysql数据库
		print('一共%d条数据' % self.i)


if __name__ == '__main__':
	start = time.time()
	spider = GovSpider()
	spider.run()
	end = time.time()
	print('执行时间%.2f' % (end - start))
