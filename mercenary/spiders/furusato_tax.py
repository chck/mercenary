# -*- coding: utf-8 -*-
import mojimoji
import re
from urllib import parse

import scrapy
from bs4 import BeautifulSoup

"""PagingSpider=>ProductsSpider=>CpSpider
"""


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


class FurusatoTaxCpSpider(scrapy.Spider):
    name = "furusato-tax-cp"
    allowed_domains = ["furusato-tax.jp"]
    base_url = "http://{}".format(allowed_domains[0])

    def __init__(self, product_id, *args, **kwargs):
        super(FurusatoTaxCpSpider, self).__init__(*args, **kwargs)
        self.product_id = product_id
        self.start_urls = [
            "{}/japan/prefecture/item_detail/{}".format(self.base_url, product_id),
        ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        quantity_candidate = soup.find("div", class_="floatR non_floatRsp item_text").find("dd")
        if quantity_candidate:
            qc = mojimoji.zen_to_han(quantity_candidate.text, kana=False)
            quantities = re.findall(r"\d+[mk]?[gm本個]", qc)
            print("{}:::{}".format(qc, quantities))
            # TODO: 抽出できた量のうち個数と量の単位に分けて+とxをうまく演算する処理

        else:
            print("指定タグ内に量が見つからないよ。別のところからひっぱってきてね")
            # TODO: 別のところから量を見つける処理 or 諦める
