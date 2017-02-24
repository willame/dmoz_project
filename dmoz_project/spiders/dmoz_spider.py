# -*- coding: utf-8 -*-
import scrapy
from dmoz_project.items import DmozItem


class DmozSpider(scrapy.Spider):
    # name = "dmoz"  # 唯一标识，启动spider时即指定该名称
    # allowed_domains = ["dmoz.org"]
    # start_urls = [
    #     "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
    #     "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    # ]
    #
    # def parse(self, response):
    #     for sel in response.xpath('//ul/li'):
    #         item = DmozItem()
    #         item['title'] = [i.strip() for i in sel.xpath('a/text()').extract()]
    #         item['link'] = [i.strip() for i in sel.xpath('a/@href').extract()]
    #         item['desc'] = [i.strip() for i in sel.xpath('text()').extract()]
    # item['url'] = site.xpath('a/@href').extract_first().strip()  另外一个例子，去掉空白符
    #         yield item
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
    ]

    def parse(self, response):
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(response.url, href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    # 1.以初始的URL（start_url）初始化Request，并设置回调函数。 当该request下载完毕并返回时，将生成response，并作为参数传给该回调函数。
    def parse_dir_contents(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = [i.strip() for i in sel.xpath('a/text()').extract()]
            item['link'] = [i.strip() for i in sel.xpath('a/@href').extract()]
            item['desc'] = [i.strip() for i in sel.xpath('text()').extract()]
            yield item
