import scrapy


class LagouSpider(scrapy.Spider):
    name = "lagou"

    def start_requests(self):
        yield scrapy.Request("https://www.lagou.com/", callback=self.parse)

    def parse(self, response):
        yield {}

