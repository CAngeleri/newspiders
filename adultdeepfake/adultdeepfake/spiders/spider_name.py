import scrapy


class SpiderNameSpider(scrapy.Spider):
    name = "spider_name"
    allowed_domains = ["adultdeepfakes.com"]
    start_urls = ["https://adultdeepfakes.com/top-rated/"]

    def parse(self, response):
        pass
