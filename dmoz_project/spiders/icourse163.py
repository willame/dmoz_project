# -*- coding: utf-8 -*-
import scrapy
from smtplib import SMTP as smtp


class Icourse163Spider(scrapy.Spider):
    name = "icourse163"
    allowed_domains = ["icourse163.org"]
    start_urls = ['http://login.icourse163.org/reg/icourseLogin.do']

    def parse(self, response):
        form_data = {
            'returnUrl': 'aHR0cDovL3d3dy5pY291cnNlMTYzLm9yZy8 =',
            'failUrl': 'aHR0cDovL3d3dy5pY291cnNlMTYzLm9yZy9tZW1iZXIvbG9naW4uaHRtP2VtYWlsRW5jb2RlZD1OVE0xTURNMk5qSTRRSEZ4TG1OdmJRPT0 =',
            'savelogin': 'false',
            'oauthType': '',
            'username': '535036628@qq.com',
            'passwd': 'aikechengp'
        }
        return scrapy.FormRequest.from_response(response, formdata=form_data, callback=self.after_login)

    def after_login(self, response):
        self.logger.info('++++++', response.url)
        self.logger.info('++++++', response.body)
        return

    @staticmethod
    def close(spider, reason):
        s = smtp('smtp.163.com', 25)
        s.login('bboyxiangkai@163.com', '*****')
        s.sendmail('bboyxiangkai@163.com', ('535036628@qq.com',), 'From:bboyxiangkai@163.com\r\nTo:535036628@qq.com\r\nSubject:Scrapy Status\r\n\r\n' + str(reason))
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)