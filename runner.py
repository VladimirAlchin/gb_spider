from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from book_labirint import settings
from book_labirint.spiders.labirint import LabirintSpider
from book_labirint.spiders.book24 import Book24Spider


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # process.crawl(LabirintSpider)

    process.crawl(Book24Spider)

    process.start()
