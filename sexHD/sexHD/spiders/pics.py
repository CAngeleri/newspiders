import scrapy
import datetime


class PicsSpider(scrapy.Spider):
    name = "pics"
    start_urls = ["https://www.sexhd.pics/"]

    def __init__(self, *args, **kwargs):
        super(PicsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        galleries = response.xpath('//div[@class="photo1"]/a/@href').getall()
        if galleries:
            for gallery in galleries:
                url = response.urljoin(gallery)
                yield scrapy.Request(url=url, callback=self.parse_gallery)

        next_page = response.xpath('//div[@class="pag"]/a[contains(text(), "Next")]/@href').get()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_gallery(self,response):
        images = response.xpath('//div[@class="relativetop"]/a/@href').getall()
        if images:
            for image in images:
                image_url = response.urljoin(image)
        
                title = response.xpath("/html/head/title/text()").get()
                tags = response.xpath('//h5[1]/a/text()').getall()

                domain = "sexhd.pics"
                page_url = response.url
                date_scrapped = datetime.datetime.now()

                if image_url.endswith('.jpg'):
                    data_object = {
                        "title": title,
                        "date_added_to_site": None,
                        "tags": tags,
                        "image_url": image_url,
                        "domain": domain,
                        "page_url": page_url,
                        "date_scraped": str(date_scrapped),
                    }
                    yield data_object