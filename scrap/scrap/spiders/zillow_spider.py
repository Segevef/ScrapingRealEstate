import scrapy
from scrap.items import HomeListing
import re
from babel.numbers import parse_number
import pandas as pd
from scrapy.crawler import CrawlerProcess


BASE_URL = 'http://zillow.com'


class ZillowScraper(scrapy.Spider):
    name = 'zillow'

    def __init__(self, *args, **kwargs):
        super(ZillowScraper, self).__init__(*args, **kwargs)
        #  Arguments are city and state
        #  Todo: search by zip code
        #  Todo: find nearby zip codes (neighbours)
        city = kwargs.get('city')
        state = kwargs.get('state')

        if not city:
            raise ValueError('city parameter not defined')
        if not state:
            raise ValueError('state parameter not defined')
        self.city = city
        self.state = state

    def start_requests(self):
        url = BASE_URL
        city = self.city
        state = self.state
        if city is not None and state is not None:
            # url = url + '/homes/' + city + '-' + state
            url = 'https://www.zillow.com/homes/alabma-birmingham/'
        yield scrapy.Request(url=url, callback=self.parse)
        # yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        #  Grab all results on page
        homes = response.css('ul.photo-cards > li')
        for home in homes:
            listing = HomeListing()
            listing['link'] = BASE_URL + home.css('a.hdp-link::attr(href)').extract_first()
            article = home.css('article.zsg-photo-card.photo-card')
            listing['latitude'] = int(article.xpath('@data-latitude').extract_first())
            listing['longitude'] = int(article.xpath('@data-longitude').extract_first())
            listing['zid'] = int(article.xpath('@data-zpid').extract_first())
            listing['pgapt'] = article.xpath('@data-pgapt').extract_first()
            listing['sgapt'] = article.xpath('@data-sgapt').extract_first()

            #  extract data from the card it self (zillow card)
            address_info = article.css('.zsg-photo-card-content > span > span')
            for entry in address_info:
                address_type = entry.xpath('@itemprop').extract_first()
                if address_type == 'streetAddress':
                    listing['street_address'] = entry.xpath('text()').extract_first()
                elif address_type == 'addressLocality':
                    listing['city'] = entry.xpath('text()').extract_first()
                elif address_type == 'addressRegion':
                    listing['state'] = entry.xpath('text()').extract_first()
                elif address_type == 'postalCode':
                    listing['zip_code'] = entry.xpath('text()').extract_first()
            request = scrapy.Request(listing['link'], self.parse_detailed_view)
            request.meta['listing'] = listing
            yield request

            #  Move to next page and keep scraping until pages are over
            next_page = response.css('li.zsg-pagination-next a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    @staticmethod
    def parse_detailed_view(self, response):

        listing = response.meta['listing']
        stats = response.css('span.addr_bbs::text')
        for stat in stats:
            text = stat.extract()
            ans = re.search('bed', text)
            if ans is not None:
                listing['beds'] = float(re.search('(\d\S*)', text).group())
            ans = re.search('bath', text)
            if ans is not None:
                listing['baths'] = float(re.search('(\d\S*)', text).group())
            ans = re.search('sqft', text)
            if ans is not None:
                val = re.search('(\d\S*)', text).group()
                listing['sq_feet'] = parse_number(val, 'en_US')
        price = response.css('div.main-row > span::text').extract_first()
        if price is not None:
            listing['list_price'] = parse_number(re.search('(\d\S*)', price).group(), 'en_US')
        x = pd.DataFrame(listing, columns=['z_id', 'street_address', 'city', 'state', 'zip_code', 'latitude',
                                           'longitude', 'pgapt', 'sgapt', 'link',
                                           'list_price', 'beds', 'baths', 'sq_feet'])
        yield x.to_csv("r", sep=",")

