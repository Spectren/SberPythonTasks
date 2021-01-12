import scrapy
from scrapy.http import Response
from scraper.items import ScraperItem

class ImdbSpider(scrapy.Spider):

    name = 'imdb_spider'
    allowed_domains = ['imdb.com']

    def start_requests(self):
        yield scrapy.Request('https://www.imdb.com/search/title/', callback=self.fetch_search_form)

    def fetch_search_form(self, response: Response):
        user_config = self.settings.get('user_config')
        # data = {
        #     "realm": "title",
        #     "title": user_config['title'],
        #     "release_date-min": user_config['release_date_to'],
        #     "release_date-max": user_config['release_date_from'],
        #     "user_rating-min": user_config['user_rating_min'],
        #     "user_rating-max": user_config['user_rating_max'],
        #     "num_votes-min": "",
        #     "num_votes-max": "",
        #     "keywords": "",
        #     "locations": "",
        #     "moviemeter-min": "",
        #     "moviemeter-max": "",
        #     "genres": user_config['genres'],
        #     "countries": user_config['countries'],
        #     "plot": "",
        #     "hidden-selected-text": "",
        #     "role": "",
        #     "runtime-min": "",
        #     "runtime-max": "",
        #     "my_ratings": "",
        #     "now_playing": "",
        #     "adult": "",
        #     "view": "simple",
        #     "count": "250",
        #     "sort": "moviemeter,asc"
        # }

        yield scrapy.FormRequest.from_response(response, formdata=user_config, formcss='form[method=POST]',
                                               callback=self.get_result_list)

    def get_result_list(self, response: Response):
        yield from (
            response.follow(link, callback=self.parse_movie_page)
            for link in response.css('.lister-item-header a::attr(href)').extract()
        )

    def parse_movie_page(self, response):
        item = ScraperItem()
        item['title'] = response.css('.title_wrapper > h1 ::text').extract_first()
        item['genres'] = ", ".join(response.css('div.see-more:nth-child(10) > a ::text').extract())
        item['rating'] = response.css('.ratingValue > strong:nth-child(1) > span ::text').extract_first()
        item['stars'] = ", ".join(response.css('td:nth-child(2) > a ::text').extract())
        item['type'] = '-'
        item['details'] = ''
        item['box_office'] = ''
        item['technical_spec'] = ''

        yield item