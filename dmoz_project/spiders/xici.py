# encoding=utf-8
import scrapy
from dmoz_project.items import XiciItem


class XiciSpider(scrapy.Spider):
    name = "xici"
    allowed_domains = ["xicidaili.com"]
    start_urls = ['http://xicidaili.com/']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Host': 'www.xicidaili.com',
            'Cache-Control': 'max-age=0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWQ4ZWI5ODg2NTI4ODkyZTFkMzIzYjNkNGVkNDI3YmZiBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXJ5RmVRb2E5V1UxdTVLZEQvNnpwRjh6V20xK1VhcExPWXpkYzFwZ0dVYnM9BjsARg%3D%3D--2c88e64285c7130cdb0f8ba027c7ebc79da9a22b; CNZZDATA1256960793=1987724857-1487845627-%7C1487928744',
            'Referer': 'http://www.xicidaili.com/nn/',
            'If-None-Match': 'W/"60519eb49429745a8ba20e6d6dd198c3"'
        }
        return [scrapy.Request('http://www.xicidaili.com/nn/%d' % (i,), headers=headers) for i in range(1, 5)]

    def parse(self, response):
        trs = response.xpath('//table[@id="ip_list"]/tr')
        self.logger.info('++++++ip numbers:%s, url:%s' % (len(trs), response.url))
        items = []
        for tr in trs[1:]:
            xc = XiciItem()
            xc['country'] = tr.xpath('td[1]/img/@alt')[0].extract() if tr.xpath('td[1]/img/@alt') else ''
            xc['ip'] = tr.xpath('td[2]/text()')[0].extract()
            xc['port'] = tr.xpath('td[3]/text()')[0].extract()
            xc['address'] = tr.xpath('td[4]/a/text()')[0].extract() if tr.xpath('td[4]/a/text()') else ''
            # self.logger.info('++++++address:%s' % (xc['address'],))
            xc['is_anonymous'] = tr.xpath('td[5]/text()')[0].extract()
            xc['protocol'] = tr.xpath('td[6]/text()')[0].extract()
            xc['speed'] = tr.xpath('td[7]/div/@title').re('[\d\.]+')[0]
            xc['connect_time'] = tr.xpath('td[8]/div/@title').re('[\d\.]+')[0]
            xc['alive_time'] = tr.xpath('td[9]/text()')[0].extract()
            xc['validate_time'] = tr.xpath('td[10]/text()')[0].extract()
            items.append(xc)
        return items  # 如果你pipeline只有一个，不返回也没关系；但如果你有多个pipeline就需要返回给其他的pipeline使用
