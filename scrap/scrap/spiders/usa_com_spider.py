import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "usa"

    def start_requests(self):
        urls = [
            'http://www.usa.com/birmingham-al'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'usa' + 'city' + '-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


# c = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0',
#     'FEED_FORMAT': 'csv',
#     'FEED_URI': 'output.csv',
# })
# c.crawl(QuotesSpider)
# c.start()
