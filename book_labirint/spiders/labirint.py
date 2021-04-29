import scrapy
from scrapy.http import HtmlResponse
from book_labirint.items import BookLabirintItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    full_domain = 'https://www.labirint.ru'
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D0%B5%D1%80%D1%83%D0%BC%D0%BE%D0%B2/?stype=0']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//div[contains(@data-dir, "books")]/div[@class = "product-cover"]/a/@href').getall()
        for link in links:
            yield response.follow(self.full_domain + link, callback=self.process_link)

        next_page = response.xpath('//div[contains(@class, "pagination-next")]/a[@title = "Следующая"]/@href').get()
        if next_page:
            yield response.follow(self.start_urls[0] + next_page, callback=self.parse)


    def process_link(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').get()
        rate = response.xpath('//div[@id="rate"]/text()').get()
        authors = response.xpath('//div[@class="authors"]/a/text()').getall()
        data_cost = response.xpath('//div[contains(@class, "buying-price")]/span/text()').getall()
        # TODO проверить эту часть кода
        if len(data_cost) == 2:
            data_cost = response.xpath('//div[contains(@class, "buying-price")]/span[contains(@cl'
                                       'ass, "buying-price-val")]/span/text()').getall()
        # для скидки //div[contains(@class, "buying-price")]/span/text()
        # без //div[contains(@class, "buying-price")]/span[contains(@class, "buying-price-val")]/span/text()

        item = BookLabirintItem()
        item['url'] = response.url
        item['name'] = name
        item['rate'] = rate
        item['authors'] = authors
        item['data_cost'] = data_cost

        yield item
