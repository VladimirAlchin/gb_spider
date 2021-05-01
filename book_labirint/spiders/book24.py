import scrapy
from scrapy.http import HtmlResponse
from book_labirint.items import BookLabirintItem
from bs4 import BeautifulSoup as bs

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

        next_page = response.xpath('//li[@class= "pagination__button-item"]/a[contains(@class, "_next")]/@href').get()
        next_page = response.xpath('//li[contains(@class, "pagination__button-item")]/a//@href').get()
        print(next_page)

        soup = bs(response.text, "lxml")
        al_txt = response.text
        with open('f.txt', 'w', encoding='utf-8') as f:
            f.write(al_txt)
        print(1)

        if next_page:
            yield response.follow(self.start_urls[0] + next_page, callback=self.parse)

    def process_link(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').getall()[0]
        name = name.strip(' \t\n\r')
        rate = response.xpath('//div[contains(@class, "_rate-value")]//text()').get()
        authors = response.xpath('//a[@itemprop="author"]/text()').getall()
        new_price = response.xpath('//div[@class = "item-actions__price"]/b/text()').get()
        currency = response.xpath('//div[@class = "item-actions__price"]/text()').get()
        old_price = response.xpath('//div[@class = "item-actions__price-old"]/text()').get()

        item = BookLabirintItem()
        item['url'] = response.url
        item['name'] = name
        item['rate'] = rate
        item['authors'] = authors
        if old_price:
            item['cost_old'] = old_price.split()[0]
            item['currency'] = old_price.split()[1]
        else:
            item['cost_old'] = 0
            item['currency'] = ''

        if new_price:
            item['cost_new'] = new_price
        else:
            item['cost_new'] = 0
        yield item
