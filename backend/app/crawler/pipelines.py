class ValidationPipeline:
    def process_item(self, item, spider):
        # TODO: validate item fields
        return item


class DuplicatesPipeline:
    def process_item(self, item, spider):
        # TODO: drop duplicates by source_url
        return item


class PostgresPipeline:
    def open_spider(self, spider):
        # TODO: connect DB
        pass

    def process_item(self, item, spider):
        # TODO: insert/update DB
        return item

