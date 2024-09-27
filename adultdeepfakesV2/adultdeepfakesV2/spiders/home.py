import datetime
import logging
from urllib.parse import urljoin
import scrapy
import hashlib
# from decouple import config 
# from adultdeepfakeV2.adultdeepfakeV2.json_helper import JSONHelper
# from bloom_filter import BloomFilter
# from redis_counter import RedisCounter


class HomeSpider(scrapy.Spider):
    name = "home"
    allowed_domains = ["adultdeepfakes.com"]
    start_urls = ["https://adultdeepfakes.com/top-rated/"]

    def __init__(self, *args, **kwargs):
        super(HomeSpider, self).__init__(*args, **kwargs)
        self.start_time = datetime.datetime.now()
        self.index = 1
        # self.base_path = config(
        #     "videos_json_path", default="/home/ubuntu/loti-scrapy/files/videos/"
        # )
        # self.threshold = config("threshold", default=5000, cast=int)
        # self.json_helper = JSONHelper(self.base_path, "adultdeepfakes.com", self.threshold)
        # self.bloom_filter = BloomFilter("adult-scraper:adultdeepfakes", 0.0001, 100000000)
        # self.redis_counter = RedisCounter("adultdeepfakes", "video")
        
    # def generate_hash(self, url):
    #     """Generates a SHA-256 hash of the given URL."""
    #     return hashlib.sha256(url.encode("utf-8")).hexdigest()
    
    def parse(self, response):
        """Parses the main page and extracts video items."""
        main_container = response.xpath('//div[contains(@class, "main-container")]')
        if main_container:
            self.logger.info("🕊️ Found the main-container")
            
            video_list = main_container.xpath('.//div[@class="list-videos"]//div[@id="list_videos_common_videos_list_items"]')
            if video_list:
                self.logger.info("💥 Found video list")

                for video in video_list.xpath('.//div[contains(@class, "item")]'):
                    title = video.xpath('.//a/@title').get(default='No Title')
                    video_url = urljoin(response.url, video.xpath('.//a/@href').get(default='No URL'))
                    date_found = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    image_url = video.xpath('.//a/div/img/@src').get(default='No Image URL')
                    domain = "https://adultdeepfakes.com/"

                    # Yield the video data
                    yield {
                        'id': self.index,
                        'title': title,
                        'video_url': video_url,
                        'image_url': urljoin(response.url, image_url),
                        "date_scraped": date_found,
                        "domain": domain
                    }
                    self.index += 1

                # Extract the next page URL if available
                next_page = response.xpath('//*[@id="list_videos_common_videos_list_pagination"]/div/ul/li/a[contains(text(), "Next")]/@href').get()
                if next_page:
                    next_page_url = urljoin(response.url, next_page)
                    self.logger.info(f"🔗 Found next page URL: {next_page_url}")
                    
                    # Check if URL already exists in the bloom filter
                    if not self.bloom_filter.url_exists(next_page_url):
                        yield scrapy.Request(next_page_url, callback=self.parse)
                    else:
                        self.logger.info(f"URL already exists in BloomFilter: {next_page_url}")
                else:
                    self.logger.info("❌ Next page fragment or URL not found")
            else:
                self.logger.info("❌ Video list not found in main container")
        else:
            self.logger.info("❌ Main container not found")

    def closed(self, reason):
        """Logs the closing time and duration of the spider."""
        end_time = datetime.datetime.now()
        runtime = end_time - self.start_time
        self.logger.info(f"🍐🍐🍐 Spider closed after {runtime}. Reason: {reason}")
