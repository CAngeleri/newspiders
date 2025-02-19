
BOT_NAME = "sexHD"

SPIDER_MODULES = ["sexHD.spiders"]
NEWSPIDER_MODULE = "sexHD.spiders"


ROBOTSTXT_OBEY = True

# from proxy_data import start_proxy_scheduler
# start_proxy_scheduler()

# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'

ROBOTSTXT_OBEY = False

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5  
AUTOTHROTTLE_MAX_DELAY = 45 
AUTOTHROTTLE_TARGET_CONCURRENCY = 5.0  

RETRY_ENABLED = True
RETRY_TIMES = 3  
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 403, 429, 573, 418, 404]
REACTOR_THREADPOOL_MAXSIZE = 20

# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 110,
    "sexHD.middlewares.SexhdDownloaderMiddleware": 543,
    # "sexHD.middlewares.ProxyMiddleware": 100,
}



# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
