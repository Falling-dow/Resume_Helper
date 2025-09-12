import scrapy


class ZhilianSpider(scrapy.Spider):
    name = "zhilian"

    def start_requests(self):
        yield scrapy.Request("https://www.zhaopin.com/", callback=self.parse)

    def parse(self, response):
        yield {}

