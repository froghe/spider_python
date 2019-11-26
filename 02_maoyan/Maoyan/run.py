from scrapy import cmdline

cmdline.execute('scrapy crawl maoyan'.split())
# cmdline.execute('scrapy crawl maoyan -o maoyan.csv'.split())
# cmdline.execute('scrapy crawl maoyan -o maoyan.json'.split())