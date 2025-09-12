import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    experience_level = scrapy.Field()
    industry = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field()
    source_url = scrapy.Field()
    source_platform = scrapy.Field()

