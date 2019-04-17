import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            # 'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
            'https://www.zillow.com/homes/alabma-birmingham_rb/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
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
