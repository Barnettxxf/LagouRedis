# -*- coding: utf-8 -*-

from scrapy import signals
import json
from scrapy import signals
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from LagouRedis.utils.get_ip import GetIp
from twisted.internet.error import TimeoutError

t = GetIp()
from scrapy.http import HtmlResponse

class LagouredisDownloaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        if response.status == 403:
            return request
        if response.status == 302:
            return request
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        super(RotateUserAgentMiddleware, self).__init__(user_agent)
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        print('User-Agent: ', ua)
        request.headers.setdefault('User-Agent', ua)
        # request.headers.setdefault('Refer', refer)

    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]





class RandomProxyMiddleware(object):

    ip_list = t.ip_list
    count = 0

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    @staticmethod
    def change_count():
        if RandomProxyMiddleware.count <= 200:
            RandomProxyMiddleware.count += 1
            return False
        else:
            RandomProxyMiddleware.count = 0
            return True

    def process_request(self, request, spider):
        if self.change_count():
            self.ip_list = t.ip_list
            with open('ip_list.txt', 'a') as f:
                f.write('-----------------------------------')
                for line in self.ip_list:
                    f.write(str(line))
                f.write('\n')
        ip, port = random.choice(self.ip_list)
        print('new_ip: ', 'https://' + ip + ':' + port)
        request.meta['proxy'] = 'https://' + ip + ':' + port

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)


class LagouCookiesMiddleware(object):

    cookies = [{'user_trace_token': '20180226001828-5c601f0f-6537-44be-a9c9-c1c381f97c3f', '_ga': 'GA1.2.1250218167.1519575509', 'LGUID': '20180226001829-83f7b1fb-1a47-11e8-917d-525400f775ce', 'index_location_city': '%E6%B7%B1%E5%9C%B3', 'showExpriedIndex': '1', 'showExpriedCompanyHome': '1', 'showExpriedMyPublish': '1', 'hasDeliver': '8', '_gid': 'GA1.2.1435031256.1522222631', 'JSESSIONID': 'ABAAABAAAFCAAEGB429AD4B0896694101694DC8B742D243', 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522032656,1522222631,1522228134,1522234524', '_gat': '1', 'LGSID': '20180328230149-f1306dc2-3298-11e8-a303-525400f775ce', 'PRE_UTM': '', 'PRE_HOST': '', 'PRE_SITE': '', 'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F', 'X_HTTP_TOKEN': '3dc49121699a69dc7f6f5deda3dcab57', 'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522249312', 'LGRID': '20180328230151-f23b4a97-3298-11e8-a303-525400f775ce', 'LG_LOGIN_USER_ID': 'a256bdd52416c841c9180e4fc55527d6c387f1127de852b7', '_putrc': '04201950329B43E0', 'login': 'true', 'unick': '%E5%BE%90%E9%9B%84%E5%B3%B0', 'gate_login_token': '2cc21eda284f612cb9970550a2894ca499b7fe7655bb9ca0', 'TG-TRACK-CODE': 'index_navigation', 'SEARCH_ID': '975def3a31a94383af0d3ab1b22daaa4'},
               {'user_trace_token': '20180226001828-5c601f0f-6537-44be-a9c9-c1c381f97c3f',
                '_ga': 'GA1.2.1250218167.1519575509', 'LGUID': '20180226001829-83f7b1fb-1a47-11e8-917d-525400f775ce',
                'index_location_city': '%E6%B7%B1%E5%9C%B3', 'showExpriedIndex': '1', 'showExpriedCompanyHome': '1',
                'showExpriedMyPublish': '1', '_gid': 'GA1.2.1435031256.1522222631',
                'JSESSIONID': 'ABAAABAAAFCAAEGB429AD4B0896694101694DC8B742D243',
                'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522032656,1522222631,1522228134,1522234524', '_gat': '1',
                'LGSID': '20180328230149-f1306dc2-3298-11e8-a303-525400f775ce', 'PRE_UTM': '', 'PRE_HOST': '',
                'PRE_SITE': '', 'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F',
                'X_HTTP_TOKEN': '3dc49121699a69dc7f6f5deda3dcab57', 'TG-TRACK-CODE': 'index_navigation',
                'gate_login_token': '137c4f6c5968dec680f49b5d3e970bd5da18923d93c97b72580d1aa4fa082ff0',
                'ab_test_random_num': '0', 'hasDeliver': '0',
                'LG_LOGIN_USER_ID': 'a603ea15d79edd55ca8e0220670c88564f06ee86b4f2a030bfaa4d0c28061887',
                '_putrc': '9E88F39614962A68123F89F2B170EADC', 'login': 'true',
                'unick': '%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B73159', 'SEARCH_ID': 'd46c2017686e4fffb313c9db581e69c1',
                'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522249795',
                'LGRID': '20180328230955-12824b00-329a-11e8-a307-525400f775ce'},
               {'user_trace_token': '20180226001828-5c601f0f-6537-44be-a9c9-c1c381f97c3f',
                '_ga': 'GA1.2.1250218167.1519575509', 'LGUID': '20180226001829-83f7b1fb-1a47-11e8-917d-525400f775ce',
                'index_location_city': '%E6%B7%B1%E5%9C%B3', 'showExpriedIndex': '1', 'showExpriedCompanyHome': '1',
                'showExpriedMyPublish': '1', '_gid': 'GA1.2.1435031256.1522222631',
                'JSESSIONID': 'ABAAABAAAFCAAEGB429AD4B0896694101694DC8B742D243',
                'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522032656,1522222631,1522228134,1522234524',
                'LGSID': '20180328230149-f1306dc2-3298-11e8-a303-525400f775ce', 'PRE_UTM': '', 'PRE_HOST': '',
                'PRE_SITE': '', 'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F',
                'X_HTTP_TOKEN': '3dc49121699a69dc7f6f5deda3dcab57', 'TG-TRACK-CODE': 'index_navigation',
                'gate_login_token': '137c4f6c5968dec680f49b5d3e970bd5da18923d93c97b72580d1aa4fa082ff0',
                'ab_test_random_num': '0', 'hasDeliver': '0', 'login': 'false', 'unick': '""', '_putrc': '""',
                'LG_LOGIN_USER_ID': '""', 'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522249909',
                'LGRID': '20180328231149-565e3968-329a-11e8-a307-525400f775ce',
                'SEARCH_ID': '2ca023b7df334aadb32097a094cea80e'},
               {'user_trace_token': '20180226001828-5c601f0f-6537-44be-a9c9-c1c381f97c3f',
                '_ga': 'GA1.2.1250218167.1519575509', 'LGUID': '20180226001829-83f7b1fb-1a47-11e8-917d-525400f775ce',
                'index_location_city': '%E6%B7%B1%E5%9C%B3', 'showExpriedIndex': '1', 'showExpriedCompanyHome': '1',
                'showExpriedMyPublish': '1', '_gid': 'GA1.2.1435031256.1522222631',
                'JSESSIONID': 'ABAAABAAAFCAAEGB429AD4B0896694101694DC8B742D243',
                'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522032656,1522222631,1522228134,1522234524',
                'LGSID': '20180328230149-f1306dc2-3298-11e8-a303-525400f775ce', 'PRE_UTM': '', 'PRE_HOST': '',
                'PRE_SITE': '', 'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F',
                'X_HTTP_TOKEN': '3dc49121699a69dc7f6f5deda3dcab57',
                'gate_login_token': '137c4f6c5968dec680f49b5d3e970bd5da18923d93c97b72580d1aa4fa082ff0',
                'ab_test_random_num': '0', 'hasDeliver': '0', 'login': 'false', 'unick': '""', '_putrc': '""',
                'LG_LOGIN_USER_ID': '""', '_gat': '1', 'SEARCH_ID': '70da247715664d05add308a49cdf868f',
                'TG-TRACK-CODE': 'search_code', 'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522250217',
                'LGRID': '20180328231656-0dc4f8ba-329b-11e8-b653-5254005c3644'},
               {'user_trace_token': '20180226001828-5c601f0f-6537-44be-a9c9-c1c381f97c3f',
                '_ga': 'GA1.2.1250218167.1519575509', 'LGUID': '20180226001829-83f7b1fb-1a47-11e8-917d-525400f775ce',
                'index_location_city': '%E6%B7%B1%E5%9C%B3', 'showExpriedIndex': '1', 'showExpriedCompanyHome': '1',
                'showExpriedMyPublish': '1', '_gid': 'GA1.2.1435031256.1522222631',
                'JSESSIONID': 'ABAAABAAAFCAAEGB429AD4B0896694101694DC8B742D243',
                'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522032656,1522222631,1522228134,1522234524',
                'LGSID': '20180328230149-f1306dc2-3298-11e8-a303-525400f775ce', 'PRE_UTM': '', 'PRE_HOST': '',
                'PRE_SITE': '', 'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F',
                'X_HTTP_TOKEN': '3dc49121699a69dc7f6f5deda3dcab57',
                'gate_login_token': '7a76cd53defdb8f5b007490594eddb2cb2ecb87577608fd26ee0ffabf3c2e19c',
                'ab_test_random_num': '0', 'hasDeliver': '0', '_gat': '1',
                'SEARCH_ID': '70da247715664d05add308a49cdf868f', 'TG-TRACK-CODE': 'search_code',
                'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1522250309',
                'LGRID': '20180328231828-44905e89-329b-11e8-b653-5254005c3644',
                'LG_LOGIN_USER_ID': 'c410d048602b2ea504ead9df3fbaa3a59dea13b8882bcdf22c5a7a4bc7aee16b',
                '_putrc': '9E88F39614962A68123F89F2B170EADC', 'login': 'true',
                'unick': '%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B73159'},

     ]

    def process_request(self, request, spider):
        request.cookies = random.choice(self.cookies)


