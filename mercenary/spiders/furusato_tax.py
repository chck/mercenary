# -*- coding: utf-8 -*-
import mojimoji
import re
from urllib import parse

import scrapy
from bs4 import BeautifulSoup

from mercenary.items import MercenaryItem

"""PagingSpider=>ProductSpider
"""


class FurusatoTaxPagingSpider(scrapy.Spider):
    name = "furusato-tax-paging"
    allowed_domains = ["furusato-tax.jp"]
    base_url = "http://{}".format(allowed_domains[0])

    def __init__(self, query, *args, **kwargs):
        super(FurusatoTaxPagingSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.start_urls = [
            "{}/search.html?target=1&q={}".format(self.base_url, parse.quote(query)),
        ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        products = soup.findAll("div", class_="thumbnail-pickUp-pt2 bg-normal col-xs-12")
        products = [product.find("a", target="_blank") for product in products if self.query in product.text]
        for product in products:
            product_url = "{}{}".format(self.base_url, product.attrs['href'])
            spider = FurusatoTaxProductSpider(product_url)
            yield scrapy.Request(product_url, callback=spider.parse)

        next_page = soup.find("li", class_="active").findNextSibling("li")
        # 次のページが見つからない場合は終了
        if not next_page:
            yield
        else:
            # scrapy.Requestを返すと次のCrawl対象としてEnqueueされる
            next_url = "{}{}".format(self.base_url, next_page.a['href'])
            yield scrapy.Request(next_url)


class FurusatoTaxProductSpider(scrapy.Spider):
    name = "furusato-tax-product"
    allowed_domains = ["furusato-tax.jp"]
    base_url = "http://{}".format(allowed_domains[0])

    def __init__(self, url, *args, **kwargs):
        super(FurusatoTaxProductSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            url,
        ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        title = soup.find("h1", class_="itemDitailh1_sp_fontSize mT05").text
        locality = soup.find("div", class_="titlePrefectures").text
        price = float(soup.find("div", class_="clearfix text-right mT10")
                      .find("span", class_="fs_32 text-red").text.replace(",", ""))

        quantity_candidates = soup.find("div", class_="floatR non_floatRsp item_text").find("dd")
        if quantity_candidates:
            qc = mojimoji.zen_to_han(quantity_candidates.text, kana=False)
            carelessly_quantity = sum(map(lambda q: int(q), re.findall(r"\d+", qc)))
            # TODO: 袋、尾、切、入、枚、箱、玉、肩、パック(PC)、\d+L(3L1kg, 3L4肩)、各\d+g、x\d+、小数点(1.7kg)、\d+人前、
            careful_quantities = re.findall(r"\d+[mk]?[lg㎏m本個]", qc)
            # print("{}:::{}".format(qc, careful_quantities))
            # TODO: 抽出できた量のうち個数と量の単位に分けて+とxをうまく演算する処理
            return MercenaryItem(title=title,
                                 locality=locality,
                                 url=response.url,
                                 cp=round(price / carelessly_quantity, 2),
                                 quantity=carelessly_quantity,
                                 price=price,
                                 careful_quantities=careful_quantities,
                                 raw=qc)
        else:
            print("指定タグ内に量が見つからないよ。別のところからひっぱってきてね")
            # TODO: 別のところから量を見つける処理 or 諦める
