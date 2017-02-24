# -*- coding:utf-8 -*-
from .dbutils import DB_Utils
import requests

db_config = {
    'user': 'root',
    'password': 'root',
    'database': 'dmozdb'
}
PER_QUERY_COUNT = 500
UNAVAILABLE_FLAG = 0


def counter(start_at=0):
    count = [start_at]

    def incr():
        count[0] += 1
        return count[0]

    return incr


# 定义方法使用代理打开链接


def use_proxy(browser, proxy, url):
    # Open browser with proxy
    # 用代理打开浏览器
    # 访问之后就切换代理ip
    # 注意传入的browser其实是selenium的webdriver生成的一个浏览器对象
    # browser = webdriver.Chrome()
    # 先获取浏览器档案
    profile = browser.profile
    # 设置档案代理类型
    profile.set_preference('network.proxy.type', 1)
    # 设置档案http代理
    profile.set_preference('network.proxy.http', proxy[0])
    # 设置代理端口
    profile.set_preference('network.proxy.http_port', int(proxy[1]))
    # 设置网页图像显示
    profile.set_preference('permissions.default.image', 2)
    # 更新档案
    profile.update_preferences()
    browser.profile = profile
    # 用浏览器打开链接
    browser.get(url)
    # 设置超时时间
    browser.implicitly_wait(30)
    return browser


# 这个单例模型用于获取ip的类继承
class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class GetIps(object):
    def __init__(self):
        self._db = DB_Utils(db_config)
        self._available_ip_count = int(self._db.query('select count(*) from `xici` where available=1')[0][0])
        self.ips = []
        index = 0

        while index <= self._available_ip_count + PER_QUERY_COUNT:
            ips = self._db.query('select id, ip, port, protocol from `xici` where available=1 limit %d, %d ' % (index, PER_QUERY_COUNT))
            index += PER_QUERY_COUNT
            self.ips.extend(ips)

    def judge_ip(self, proxy, is_http=True):
        http_url = "http://www.baidu.com/"
        https_url = "https://www.alipay.com/"
        url = http_url if is_http else https_url
        try:
            response = requests.get(url, proxies=proxy, timeout=20)
        except Exception as e:
            print("Request Error:", e)
            return False
        else:
            if 300 > response.status_code >= 200:
                print('Effective proxy', proxy.values())
                return True
            else:
                print('Else response status code: ', response.status_code)
                return False

    # 这是核心方法，这个类就是用来获取可用且高速的代理ip
    def get_ips(self):
        unavailable_ids = []
        http_ips = []
        https_ips = []
        for ip in self.ips:
            protocol = ip[3]
            proxy = {protocol: 'http://%s:%s' % (ip[1], ip[2])}
            if not self.judge_ip(proxy, protocol.endswith('P')):
                unavailable_ids.append((UNAVAILABLE_FLAG, ip[0]))
            elif self.judge_ip(proxy, protocol.endswith('P')) and protocol.endswith('P'):
                http_ips.append(proxy)
            else:
                https_ips.append(proxy)
            if len(unavailable_ids) > PER_QUERY_COUNT:
                self._db.execute_many('update `xici` set available=%s where id=%s', unavailable_ids)
                unavailable_ids.clear()
        if unavailable_ids:
            self._db.execute_many('update `xici` set available=%s where id=%s', unavailable_ids)
            unavailable_ids.clear()
        print("+++++Got %d available ips." % (len(http_ips) + len(https_ips)))
        return {'http': http_ips, 'https': https_ips}
