import scrapy
from scrapy.http import HtmlResponse
from book_labirint.items import BookLabirintItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    full_domain = 'https://book24.ru'
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D0%B5%D1%80%D1%83%D0%BC%D0%BE%D0%B2']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//article/div[@class = "product-card__image-holder"]/a/@href').getall()
        print()
        for link in links:
            yield response.follow(self.full_domain + link, callback=self.process_link)

        # next_page = response.xpath('//div[contains(@class, "pagination-next")]/a[@title = "Следующая"]/@href').get()
        # if next_page:
        #     yield response.follow(self.start_urls[0] + next_page, callback=self.parse)

    def process_link(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').getall()[0]
        name = name.strip(' \t\n\r')
        rate = response.xpath('//div[contains(@class,"rating__rate-value")]/text()').get()
        authors = response.xpath('//a[@itemprop="author"]/text()').getall()
        new_price = response.xpath('//div[@class = "item-actions__price"]/b/text()').get()
        currency = response.xpath('//div[@class = "item-actions__price"]/text()').get()
        old_price = response.xpath('//div[@class = "item-actions__price-old"]/text()').get()
        # data_cost = response.xpath('//div[contains(@class, "buying-price")]/span/text()').getall()
        # if len(data_cost) == 2:
        #     data_cost = response.xpath('//div[contains(@class, "buying-price")]/span[contains(@cl'
        #                                'ass, "buying-price-val")]/span/text()').getall()
        # для скидки //div[contains(@class, "buying-price")]/span/text()
        # без //div[contains(@class, "buying-price")]/span[contains(@class, "buying-price-val")]/span/text()

        item = BookLabirintItem()
        item['url'] = response.url
        item['name'] = name
        item['rate'] = rate
        item['authors'] = authors
        item['cost_old'] = old_price.split()[0]
        item['cost_new'] = new_price
        item['currency'] = old_price.split()[1]
        # item['data_cost'] = data_cost
        print()
        yield item
