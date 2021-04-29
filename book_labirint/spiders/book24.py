import scrapy


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['https://book24.ru/']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D0%B5%D1%80%D1%83%D0%BC%D0%BE%D0%B2']

    def parse(self, response):
        pass
