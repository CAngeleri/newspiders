"""
    How to run spider : 
        cd newspiders/adultdeepfake
        run command "scrapy crawl adultdeepfake"
        output : 
            display Json obj in terminal 
            save doc to output.json
"""

import scrapy
from urllib.parse import urljoin
from datetime import datetime

class AdultdeepfakeSpider(scrapy.Spider):
    name = "adultdeepfake"
    index = 1
    max_items = 300 

    def __init__(self, *args, **kwargs):
        super(AdultdeepfakeSpider, self).__init__(*args, **kwargs)
        # Record the start time
        self.start_time = datetime.now()

    def start_requests(self):
        start_url = "https://adultdeepfakes.com/top-rated/"
        yield scrapy.Request(start_url, self.parse)

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

                # Check if the "Load More" button or next page link exists
                next_page = response.xpath('//*[@id="list_videos_common_videos_list_pagination"]/div/ul/li[14]/a/@href').get()
                if next_page or main_container:
                    next_page_url = urljoin(response.url, next_page)
                    yield scrapy.Request(next_page_url, callback=self.parse)
                    
            else:
                self.logger.info("❌ video list not found")
                print("❌ video list not found")

        else:
            self.logger.info("❌ main-container not found")
            print("❌ main-container not found")

    def closed(self, reason):
        # Record the end time and calculate runtime
        end_time = datetime.now()
        runtime = end_time - self.start_time
        self.logger.info(f"🍐🍐🍐🍐🍐🍐🍐🍐🍐 Spider closed after {runtime}")
        print(f"Spider closed after {runtime}")
