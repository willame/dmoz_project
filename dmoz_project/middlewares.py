# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from .proxy import GetIps
import logging


class DmozProjectSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 首先获取高速可用的代理ip
ips = GetIps().get_ips()


class ProxyMiddleware(object):
    http_n = 0
    https_n = 0

    def process_request(self, request, spider):
        if request.url.startswith("http://"):
            n = ProxyMiddleware.http_n
            n = n if n < len(ips['http']) else 0
            request.meta['proxy'] = ips['http'][n]
            logging.info('[ProxyMiddleware] Set proxy %s' % (ips['http'][n],))
            ProxyMiddleware.http_n = n + 1

        if request.url.startswith("https://"):
            n = ProxyMiddleware.https_n
            n = n if n < len(ips['https']) else 0
            request.meta['proxy'] = ips['https'][n]
            logging.info('[ProxyMiddleware] Set proxy %s' % (ips['https'][n],))
            ProxyMiddleware.https_n = n + 1
        pass