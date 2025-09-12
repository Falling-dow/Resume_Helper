import scrapy


class LiepinSpider(scrapy.Spider):
    name = "liepin"

    def start_requests(self):
        yield scrapy.Request("https://www.liepin.com/", callback=self.parse)

    def parse(self, response):
        yield {}

