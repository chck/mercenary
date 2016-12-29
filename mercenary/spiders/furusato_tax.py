# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from bs4 import BeautifulSoup



class FurusatoTaxPagingSpider(scrapy.Spider):
    name = "furusato-tax-paging"
    allowed_domains = ["furusato-tax.jp"]
    base_url = "http://{}".format(allowed_domains[0])

    start_urls = [
        "{}/search.html?target=1&q={}".format(base_url, parse.quote("いくら")),
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        next_page = soup.find('li', class_='active').findNextSibling('li')
        # 次のページが見つからない場合は終了
        if not next_page:
            yield

        path = next_page.a['href']
        url = "{}{}".format(self.base_url, path)
        print(url)

        # scrapy.Requestを返すと次のCrawl対象としてEnqueueされる
        next_crawl_page = scrapy.Request(url)
        yield next_crawl_page


class FurusatoTaxProductsSpider(scrapy.Spider):
    name = "furusato-tax-products"
    allowed_domains = ["furusato-tax.jp"]
    base_url = "http://{}".format(allowed_domains[0])

    def __init__(self, page_path, *args, **kwargs):
        super(FurusatoTaxProductsSpider, self).__init__(*args, **kwargs)
        self.page_path = page_path
        self.start_urls = [
            "{}/search.html{}".format(self.base_url, page_path),
        ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        products = soup.findAll("div", class_="thumbnail-pickUp-pt2 bg-normal col-xs-12")
        products = [product.find("a", target="_blank") for product in products]
        for product in products:
            # if "セット" in product.text:
            # print(product.text)
            # print(product.attrs['href'])
            url = "{}{}".format(self.base_url, product.attrs['href'])
            yield scrapy.Request(url)

