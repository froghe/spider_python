import csv
import random
import time
import requests
from lxml import etree
from selenium import webdriver

class JDSpider(object):
	def __init__(self):
		self.url = 'https://www.jd.com'
		self.options = webdriver.ChromeOptions()
		self.options.add_argument('--headless')
		self.dr = webdriver.Chrome(options=self.options)
		self.i = 0
		self.L = []

	def search_commodity(self, word):
		'''
		首页搜索商品
		:param word:
		:return:
		'''
		self.dr.get(self.url)
		self.dr.find_element_by_id('key').send_keys(word)
		self.dr.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
		time.sleep(3)

	def get_commodity_link(self):
		'''
		获取每个商品详情页的链接，和信息
		:return:
		'''
		self.dr.execute_script('window.scrollTo(0,document.body.scrollHeight)')
		time.sleep(1.5)
		xpath_bds = '//*[@id="J_goodsList"]/ul/li'
		l_list = self.dr.find_elements_by_xpath(xpath_bds)
		for l in l_list:
			item = {}
			L = l.text.split('\n')
			# 价格 + 超市 + 评论 + 店铺
			if L[1] == '京东超市':
				item['price'] = L[0]
				item['shop'] = L[1]
				item['comment'] = L[3]
				item['store'] = L[4]
			elif L[1].startswith('￥'):
				item['price'] = L[0]
				item['shop'] = None
				item['comment'] = L[3]
				item['store'] = L[4]
			else:
				item['price'] = L[0]
				item['shop'] = None
				item['comment'] = L[2]
				item['store'] = L[3]

			# 获取元素节点属性值
			link = l.find_elements_by_xpath('./div/div[3]/a')[0].get_attribute('href')
			item = self.parse_html(link, item)
			time.sleep(random.uniform(1,3))  # 每爬取一个商品详情页面休眠
			self.i += 1
			self.dict_list(item)

		with open('jd.csv', 'w', encoding='gbk', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(self.L)

	def dict_list(self, item):
		t = (
			# 名称 + 编号 + 口味 + 价格 + 店铺 + 评论 + 毛重 + 产地 + 类别 + 超市 + 规格
			item['name'],
			item['number'],
			item['taste'],
			item['price'],
			item['store'],
			item['comment'],
			item['weight'],
			item['address'],
			item['type'],
			item['shop'],
			item['specification'],
		)
		self.L.append(t)

	def get_html(self, url):
		'''
		商品详情页面请求响应
		:param url:
		:return:
		'''
		headers = {
			"cookie": "__jdu=192522249; areaId=19; ipLoc-djd=19-1607-3638-0; PCSYCityID=CN_440000_440300_440304; shshshfpa=98d6498d-cbc6-6ff6-6756-d0b7ad5b5f55-1574838028; shshshfpb=uVkMdJJZCVytQ8bOL8A%20srQ%3D%3D; unpl=V2_ZzNtbUVUFBd2X0IEK0wIUGJTEFRLVUMcJgsSVHgZDARlBBtdclRCFX0URlRnGloUZwcZXUZcQRJFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsRXwFkABFYSmdzEkU4dlF7EFgDZDMTbUNnAUEpD0FRfRxbSGcLEVlBVEAQfThHZHg%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_62f32f5aaded4a388318b2e121a03681|1574838939322; 3AB9D23F7A4B3C9B=P4A45YPZL2AMJA5GKE4LE5E2BSU3OF64RGK2MWUVV6NBGAK6MI7BFBTJY4LL2USEBULIXOXSNXJNOZ3G6P75TMQZBA; __jdc=122270672; shshshfp=81e364fde1a6c71c6a1b8ab361d0131d; __jda=122270672.192522249.1574838022.1574838024.1574843220.2; __jdb=122270672.6.192522249|2.1574843220; shshshsID=78e3a185fbf6678262217b5ffab03d0e_6_1574844528879",
			"referer": "https://search.jd.com/Search?keyword=%E8%BE%A3%E6%9D%A1&enc=utf-8&wq=%E8%BE%A3%E6%9D%A1&pvid=b74b6312ef2442518aeb8f50754efdfb",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
		}
		return requests.get(url=url, headers=headers).text

	def parse_html(self, link, item):
		'''
		解析详情页面信息
		:param link:
		:param item:
		:return:
		'''
		html = self.get_html(link)
		xpath_bds = '//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]'
		parse_html = etree.HTML(html)
		r_list = parse_html.xpath(xpath_bds)
		for r in r_list:
			# 名称 + 编号 + 毛重 + 产地 + 类别 + 口味 + 规格
			name = r.xpath('./li[1]/@title')
			number = r.xpath('./li[2]/@title')
			weight = r.xpath('./li[3]/@title')
			address = r.xpath('./li[4]/@title')
			type = r.xpath('./li[5]/@title')
			taste = r.xpath('./li[6]/@title')
			specification = r.xpath('./li[7]/@title')
			item['name'] = [name[0].strip() if name else None][0]
			item['number'] = [number[0].strip() if number else None][0]
			item['weight'] = [weight[0].strip() if weight else None][0]
			item['address'] = [address[0].strip() if address else None][0]
			item['type'] = [type[0].strip() if type else None][0]
			item['taste'] = [taste[0].strip() if taste else None][0]
			item['specification'] = [specification[0].strip() if specification else None][0]
		return item

	def run(self):
		word = input('请输入要搜索的内容：')  # 辣条
		self.search_commodity(word)
		self.get_commodity_link()
		print(self.i)

if __name__ == '__main__':
	start = time.time()
	spider = JDSpider()
	spider.run()
	end = time.time()
	print('下载完成，执行时间：%.2f' % (end-start))

