import scrapy


class ScraperItem(scrapy.Item):
    title = scrapy.Field()
    genres = scrapy.Field()
    rating = scrapy.Field()
    stars = scrapy.Field()
    type = scrapy.Field()
    details = scrapy.Field()
    box_office = scrapy.Field()
    technical_spec = scrapy.Field()
