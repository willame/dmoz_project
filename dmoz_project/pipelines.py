# -*- coding: utf-8 -*-
import codecs
import json
from twisted.enterprise import adbapi
import MySQLdb  # 安装pythonclient即可
import MySQLdb.cursors
from mysql import connector


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JsonWithEncodingPipeline(object):
    # 保存到文件中对应的class
    # 1、在settings.py文件中配置
    # 2、在自己实现的爬虫类中yield item,会自动执行

    def __init__(self):
        self.file = codecs.open('dmoz2.json', 'w', encoding='utf-8')  # 保存为json文件

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"  # 转为json的
        self.file.write(line)  # 写入文件中
        return item

    def spider_closed(self, spider):  # 爬虫结束时关闭文件
        self.file.close()


class Dmoz2StorePipline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        # 1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
        # 2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
        # 3、可以通过类来调用，就像C.f()，相当于java中的静态方法
        db_params = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DATABASE'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        db_pool = adbapi.ConnectionPool('MySQLdb', **db_params)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(db_pool)  # 相当于db_pool付给了这个类，self中可以得到

    # 写入数据库中
    def _conditional_insert(self, tx, item):
        sql = "insert into dmoz(title,link, dmoz_desc) values(%s, %s, %s)"
        params = (item['title'], item['link'], item['desc'])
        print('+++++++++++++++++++Saving to database,title is ', item['title'])
        tx.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, failure, item, spider):
        print('+++++', failure)

    def process_item(self, item, spider):
        query = self.db_pool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item


class XiciPipeline(object):
    xici_buffer = []

    def process_item(self, item, spider):
        params = (item['country'], item['ip'], item['port'], item['address'], item['is_anonymous'],
                  item['protocol'], item['speed'], item['connect_time'], item['alive_time'], item['validate_time'])
        self.xici_buffer.append(params)
        if len(self.xici_buffer) > 2000:
            self.save_to_db()
            return item
        return item

    def close_spider(self, spider):
        if self.xici_buffer:
            self.save_to_db()
        self.client.close()

    def save_to_db(self):
        # mysql_config = spider.setting.get('mysql_dic') 这种是将数据配置到一个dict中，然后传入**mysql_config
        conn = connector.connect(user='root', password='root', database='dmozdb')
        sql = "insert into xici_crawl(country, ip, port, address, is_anonymous, protocol, speed, connect_time, alive_time, " \
              "validate_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        print('+++++++++++++++++++Inserting %d items to database.' % (len(self.xici_buffer,)))
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, self.xici_buffer)
        except Exception as e:
            print('+++Insert Error:', e)
            conn.rollback()
        else:
            self.xici_buffer.clear()
            conn.commit()  # 必须要commit
        finally:
            cursor.close()
            conn.close()
