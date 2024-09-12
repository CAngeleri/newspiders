import scrapy
from urllib.parse import urljoin
from datetime import datetime

class AdultdeepfakeNewSpider(scrapy.Spider):
    name = "adultdeepfake_new"
    index = 1
    max_items = 300

    def __init__(self, *args, **kwargs):
        super(AdultdeepfakeNewSpider, self).__init__(*args, **kwargs)
        self.start_time = datetime.now()

    def start_requests(self):
        start_url = "https://adultdeepfakes.com/videos/#videos"
        yield scrapy.Request(start_url, self.parse)

    def parse(self, response):
        # Refined XPath to select the main-container div
        main_container = response.xpath('/html/body/div[2]//div[contains(@class, "main-container")]')
        
        if main_container:
            self.logger.info("🕊️ Found the main-container with updated XPath")
            print("🕊️ Found the main-container with updated XPath")

            # Select the box that holds the videos
            video_box = main_container.xpath('//*[@id="list_videos_latest_videos_list_items"]')
            
            if video_box:
                self.logger.info("💥 Found video box")
                print("💥 Found video box")

                for video in video_box.xpath('.//div[contains(@class, "item")]'):
                    title = video.xpath('.//a/@title').get(default='No Title')
                    video_url = urljoin(response.url, video.xpath('.//a/@href').get(default='No URL'))
                    date_found = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    image_url = video.xpath('.//a/div/img/@src').get(default='No Image URL')
                    domain = "https://deepfakes.com/new/"

                    yield {
                        'id': self.index,
                        'title': title,
                        'video_url': video_url,
                        'image_url': urljoin(response.url, image_url),
                        "date_scraped": date_found,
                        "domain": domain
                    }
                    self.index += 1

                # Extract the next page URL
                next_page = response.xpath('//*[@id="list_videos_latest_videos_list_pagination"]/div/ul/li[14]/a/@href').get()
                
                # Log the next page URL
                self.logger.info(f"🔗 Found next page URL: {next_page}")
                print(f"🔗 Found next page URL: {next_page}")

                if next_page or main_container:
                    next_page_url = urljoin(response.url, next_page)
                    yield scrapy.Request(next_page_url, callback=self.parse)
                else:
                    self.logger.info("❌ Next page link not found")
                    print("❌ Next page link not found")
            else:
                self.logger.info("❌ Video box not found")
                print("❌ Video box not found")
        else:
            self.logger.info("❌ Main container not found with updated XPath")
            print("❌ Main container not found with updated XPath")

    def closed(self, reason):
        end_time = datetime.now()
        runtime = end_time - self.start_time
        self.logger.info(f"🍐 Spider closed after {runtime} on new page")
        print(f"Spider closed after {runtime} on new page")
