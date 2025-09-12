import scrapy


class BossSpider(scrapy.Spider):
    name = "boss"

    def start_requests(self):
        # TODO: seed URLs
        yield scrapy.Request("https://www.zhipin.com/", callback=self.parse)

    def parse(self, response):
        # TODO: parse job listings
        yield {}

