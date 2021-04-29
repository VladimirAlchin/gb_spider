# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.http import HtmlResponse


class BookLabirintPipeline:
    def __init__(self):
        self.client = MongoClient('localhost:27017')
        self.db = self.client['gb_parser']

    def process_item(self, item, spider):
        if spider.name == 'LabirintSpider':
            if len(item['data_cost']) == 2:
                item['cost_old'] = float(item['data_cost'][0])
                item['cost_new'] = 0
                item['currency'] = item['data_cost'][1]
                item['cost_status'] = '1'
            elif len(item['data_cost']) == 1:
                item['cost_old'] = 0
                item['cost_new'] = 0
                item['currency'] = ''
                item['cost_status'] = '0'
            else:
                item['cost_old'] = float(item['data_cost'][0])
                item['cost_new'] = float(item['data_cost'][1])
                item['currency'] = item['data_cost'][2]
                item['cost_status'] = '1'
            del item['data_cost']
        self.db[spider.name].insert_one(item)

        return item
