from w3lib.url import url_query_cleaner
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

def process_links(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link

class WebscraperCrawler(CrawlSpider):
    name = "webscraper"
    
    custom_settings = {
        'HTTPCACHE_DIR': './httpcache',
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 0,
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 1,
    }

    start_urls = ['https://webscraper.io/test-sites/e-commerce/allinone']
    allowed_domains = ['webscraper.io']
    
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths='//ul[@class="nav"]//li/a[contains(@class, "category-link ")]'),
            callback="parse_item",
            process_links=process_links,
            follow=True,
        ),
    )
    
    def parse_item(self, response):
        return {
            'url': response.url,
            'status': response.status,
            'image_url':response.selector.xpath('//img/@src').get(),
            'price':response.selector.xpath('//h4[contains(@class, "price")]/text()').get(),
            'title':response.selector.xpath('//h4/a[@class="title"]/text()').get(),
            'product_url':response.selector.xpath('//h4/a[@class="title"]/@href').get(),
            'description':response.selector.xpath('//p[@class="description"]/text()').get(),
            'review':response.selector.xpath('//div[@class="ratings"]/p/text()').get(),
            'ratings':response.selector.xpath('//div[@class="ratings"]/p[boolean(@data-rating)]/@data-rating').get(),
        }    