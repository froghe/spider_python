import re
from urllib import parse
import requests
from bs4 import BeautifulSoup

class YoudaoSpider(object):
	def __init__(self):
		self.url = 'http://m.youdao.com/translate'
		self.headers = {
			"Cookie": "OUTFOX_SEARCH_USER_ID=-781697071@10.108.160.19; OUTFOX_SEARCH_USER_ID_NCOO=860318458.8866111; YOUDAO_MOBILE_ACCESS_TYPE=0; ___rl__test__cookies=1575169038493; _yd_btn_fanyi_1=true",
			"Referer": "http://m.youdao.com/translate?vendor=fanyi.web",
			"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36",
		}

	def get_html(self, inputtext):
		data = {
			"inputtext": inputtext,
			"type": "AUTO"
		}
		html = requests.post(
			url=self.url,
			data=data,
			headers=self.headers
		).text
		bs = BeautifulSoup(html, 'lxml')
		# result = bs.select('ul[id="translateResult"]')[0].get_text().strip()
		result = bs.select_one('#translateResult').get_text().strip()
		return result

	def run(self):
		while True:
			word = input('请输入要翻译的单词：')
			if word == '':
				break
			# inputtext = parse.quote(word)  # 不需要编码
			result = self.get_html(word)
			print(result)

if __name__ == '__main__':
	spider = YoudaoSpider()
	spider.run()
