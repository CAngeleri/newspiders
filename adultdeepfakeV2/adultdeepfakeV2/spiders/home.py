import datetime
import logging
from urllib.parse import urljoin
import scrapy
import hashlib
from decouple import config
from json_helper.manage import JSONHelper
from bloom_filter import BloomFilter
from redis_counter import RedisCounter


class HomeSpider(scrapy.Spider):
    name = "home"
    allowed_domains = ["adultdeepfake.com"]
    start_url = "https://adultdeepfakes.com/top-rated/"

    def __init__(self, *args, **kwargs):
        super(HomeSpider, self).__init__(*args, **kwargs)
        self.base_path = config(
            # "videos_json_path", default="/home/ubuntu/loti-scrapy/files/videos/"
        )
        self.threshold = config("threshold", default=5000, cast=int)
        self.json_helper = JSONHelper(self.base_path, "adultdeepfake.com", self.threshold)
        self.bloom_filter = BloomFilter("adult-scraper:adultdeepfake", 0.0001, 100000000)
        self.redis_counter = RedisCounter("adultdeepfake", "video")
        
    def generate_hash(self, url):
        url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return url_hash
    
    def parse(self, response):
        # Check if main-container exists
        main_container = response.xpath('/html/body/div[2]/div[3]/div[1]/div[contains(@class, "main-container")]')
        if main_container:
            self.logger.info("🕊️ Found the main-container")
            print("🕊️ Found the main-container")
            
            # Extract the list-videos container
            video_list = main_container.xpath('.//div[@class="list-videos"]//div[@id="list_videos_common_videos_list_items"]')
            if video_list:
                self.logger.info("💥 Found video list")
                print("💥 Found video list")

                # Extract video items
                for video in video_list.xpath('.//div[contains(@class, "item")]'):
                    title = video.xpath('.//a/@title').get(default='No Title')
                    video_url = urljoin(response.url, video.xpath('.//a/@href').get(default='No URL'))
                    date_found = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    image_url = video.xpath('.//a/div/img/@src').get(default='No Image URL')
                    domain =  "https://adultdeepfakes.com/"

                    yield {
                        'id': self.index,
                        'title': title,
                        'video_url': video_url,
                        'image_url': urljoin(response.url, image_url),
                        "date_scraped": date_found,
                        "domain": domain
                    }
                    self.index += 1
"""
    def parse(self, response):
        items = response.xpath("//div[@class='thmbclck']/a/@href").extract_first()
        for item in items:
            url = "https://anyporn.com" + item

            if self.bloom_filter.url_exists(url):
                self.logger.info(f"URL already exists: {url}")
                continue

            yield scrapy.Request(url=url, callback=self.parse)

        next_page_url = response.xpath("//li[@class='nopop next']").extract_first()

        if next_page_url:
            yield scrapy.Request(
                url="https://anyporn.com/newest" + next_page_url, callback=self.parse
            )
"""
                # Check if the "Load More" button or next page link exists
                next_page = response.xpath('//*[@id="list_videos_common_videos_list_pagination"]/div/ul/li[14]/a/@href').get()
                
                if next_page :
                    next_page_url = urljoin(response.url, next_page)
                    self.logger.info(f"🔗 Found next page URL: {next_page_url}")
                    yield scrapy.Request(next_page_url, callback=self.parse)
                else:
                    self.logger.info("❌ Next page fragment or URL not found")

        else:
            self.logger.info("❌ main-container not found")
            print("❌ main-container not found")

    def closed(self, reason):
        end_time = datetime.now()
        runtime = end_time - self.start_time
        self.logger.info(f"🍐🍐🍐🍐🍐🍐🍐🍐🍐 Spider closed after {runtime}")
        print(f"Spider closed after {runtime}")
