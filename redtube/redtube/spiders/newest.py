import scrapy
import json
import logging
import datetime
import re

class NewestSpider(scrapy.Spider):
    name = "newest"
    allowed_domains = ["www.redtube.com"]
    start_urls = ["https://www.redtube.com/newest"]

    def __init__(self, *args, **kwargs):
        super(NewestSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        videos = response.xpath('//div[@class="video_title"]/a/@href').getall()

        for video in videos:
            url = response.urljoin(video)
            yield scrapy.Request(url=url, callback=self.parse_page)

        next_page = response.xpath('//*[@id="wp_navNext"]/@href').get()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_page(self, response):
        title = response.xpath("//title/text()").get()
        date_added_to_site = response.xpath(
            '//*[@id="video-infobox-wrap"]/div/div[1]/div[2]/span[2]/text()'
        ).get()
        cleaned_date = re.sub(r"^Published on\s*", "", date_added_to_site)

        tags = response.xpath(
            '//meta[@name="adsbytrafficjunkycontext"]/@data-context-tag'
        ).get()
        tags_list = tags.split(",")

        # Extract embedded URL (already in the previous code)
        video_url = response.xpath('//meta[@name="twitter:player"]/@content').get()
        if not video_url:
            # Fallback: try to extract an MP4 video file directly from the page if possible
            video_url = response.xpath('//video/source/@src').get()
        
        # If there's no direct video URL, try to get the link from a fallback player
        if not video_url:
            video_url = response.xpath('//iframe[@id="player"]/@src').get()
            # Sometimes an iframe might load the video externally, so follow the iframe URL
            if video_url:
                video_url = response.urljoin(video_url)

        domain = "redtube.com"
        page_url = response.url
        date_scrapped = datetime.datetime.now()

        # Make sure we have a valid video URL before yielding
        if video_url:
            data_object = {
                "title": title,
                "date_added_to_site": cleaned_date,
                "tags": tags_list,
                "video_url": video_url,
                "domain": domain,
                "page_url": page_url,
                "date_scraped": str(date_scrapped),
            }
            yield data_object