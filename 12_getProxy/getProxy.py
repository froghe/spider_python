import random
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class GetProxy(object):
	def __init__(self):
		self.url = 'https://www.xicidaili.com/nn/{}'
		self.ua = UserAgent()

	def get_html(self, url):
		headers = {'User-Agent': self.ua.random}
		html = requests.get(url=url, headers=headers).text
		bs = BeautifulSoup(html, 'lxml')
		tr_list = bs.find_all('tr', attrs={'class': 'odd'})
		for tr in tr_list:
			ip = tr.select('td')[1].get_text()
			port = tr.select('td')[2].get_text()
			self.test_proxy(ip, port)

	def test_proxy(self, ip, port):
		proxies = {
			'http': 'http://{}:{}'.format(ip, port),
			'https': 'https://{}:{}'.format(ip, port)
		}
		url = 'http://www.baidu.com'
		try:
			res = requests.get(url=url, proxies=proxies, timeout=5)
			if res.status_code == 200:
				print(ip, port, 'Success')
				with open('proxies.txt', 'a') as f:
					f.write(ip + ':' + port + '\n')
		except Exception as e:
			print(ip, port, 'Failed')

	def run(self):
		for pn in range(1, 1001):
			self.get_html(self.url.format(pn))
			time.sleep(random.uniform(2, 3))

if __name__ == '__main__':
	proxy = GetProxy()
	proxy.run()

