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
        item['genres'] = ", ".join(response.css('.see-more.inline.canwrap > a[href*=title_type] ::text').extract())
        item['rating'] = response.css('.ratingValue > strong > span ::text').extract_first()
        item['stars'] = ", ".join(response.css('td:nth-child(2) > a ::text').extract())
        item['type'] = '-' #Я не увидел, где это поле находится на странице
        item['details'] = {
            'Official Sites: ': ", ".join(response.css('#titleDetails >div> a[href*=offsite] ::text').extract()),
            'Country: ': ", ".join(response.css('#titleDetails > div > a[href*=country_of_origin] ::text').extract()),
            'Language: ': ", ".join(response.css('#titleDetails >div > a[href*=primary_language] ::text').extract()),
            #'Release Date: ': response.css('#titleDetails > div:nth-child(5)').extract(),
            #'Also Known As: ': response.css('div.txt-block:nth-child(6)').extract(),
            'Filming Locations: ': response.css('#titleDetails >div > a[href*=locations] ::text').extract_first()
        },
        item['box_office'] = {
            #'Opening Weekend USA: ': response.css('div.txt-block:nth-child(11)').extract(),
            #'Gross USA: ': response.css('#titleDetails > div:nth-child(12)').extract(),
            #'Cumulative Worldwide Gross: ': response.css('#titleDetails > div:nth-child(13)').extract(),
        },
        item['technical_spec'] = {
            'Runtime': response.css('.txt-block > time ::text').extract_first(),
            'Sound Mix: ': ", ".join(response.css('.txt-block > a[href*=sound_mixes] ::text').extract()),
            'Color: ': response.css('.txt-block > a[href*=colors] ::text').extract_first(),
            #'Aspect Ratio: ': response.css('div.txt-block:nth-child(24)').extract(),
        },

        yield item