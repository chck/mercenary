# -*- coding: utf-8 -*-
import scrapy


class FurusatoTaxSpider(scrapy.Spider):
    name = "furusato-tax"
    allowed_domains = ["furusato-tax.jp"]
    start_urls = ['http://furusato-tax.jp/']

    def parse(self, response):
        pass
