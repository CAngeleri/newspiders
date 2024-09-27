import scrapy
import datetime


class HomeSpider(scrapy.Spider):
    name = "home"
    allowed_domains = ["bigporn.com"]
    start_urls = ["https://www.bigporn.com/tag-celebrity/1.html"]

    # Initialize page index as a class attribute to manage URL incrementation properly
    url_idx = 1

    def parse(self, response):
        # Locate the main container
        main_container = response.xpath('/html/body/div[1]/div[3]/div[2]')

        if main_container:
            # self.logger.info('🕊️ Main Container found! 🕊️')
            # print('🕊️ Main Container found! 🕊️')

            # Select all items within the main container
            items = main_container.xpath('./ins/div')

            # Iterate over each item and extract data
            for index, item in enumerate(items, start=1):
                # self.logger.info(f'🔍 Extracting data from item {index} 🔍')
                # print(f'🔍 Extracting data from item {index} 🔍')

                # Extract desired fields from each item
                title = item.xpath('.//p[1]/text()').get(default='No title found')
                img_url = item.xpath(".//div[1]/a/img/@data-src").get(default='No image found')
                video_link = item.xpath(".//div[1]/a/@href").get(default='No image found')
                tags = item.xpath('.//p[2]/a/text()').getall()
                domain = 'bigporn.com'
                page_url = response.url
                date_scrapped = datetime.datetime.now().isoformat()

                # Yield the extracted data
                yield {
                    'title': title,
                    'img_url': img_url,
                    'video_link' : f'https://www.bigporn.com/{video_link}',
                    'tags': tags if tags else ['No tags found'],
                    'domain': domain,
                    'page_url': page_url,
                    'date_scrapped': date_scrapped
                }

            # Handle pagination by locating the next page link
            next_page = response.xpath('//li[contains(@class, "next")]/a/@href').get()  # Adjust XPath to find the actual next page link
            if next_page:
                # If the next_page is a relative URL, response.follow will handle it correctly.
                yield response.follow(next_page, callback=self.parse)

            else:
                self.logger.info('🚫 No more pages found! Stopping pagination. 🚫')
                print('🚫 No more pages found! Stopping pagination. 🚫')
        else:
            self.logger.warning('⚠️ Main Container not found! ⚠️')
            print('⚠️ Main Container not found! ⚠️')
