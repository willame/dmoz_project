# -*- coding: utf-8 -*-
import scrapy
from dmoz_project.items import DmozItem


class Dmoz2Spider(scrapy.Spider):
    name = "dmoz2"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        divs = response.xpath('//div[@class="title-and-desc"]')
        for div in divs:
            dmoz_item = DmozItem()
            dmoz_item['title'] = div.xpath('a/div/text()').extract_first()
            # self.logger.info('++++ div.xpath("a/div/text()") type is %s)', type(div.xpath('a/div/text()')))
            dmoz_item['link'] = div.xpath('a/@href').extract_first()
            dmoz_item['desc'] = div.xpath('div/text()').extract_first().strip()
            yield dmoz_item

