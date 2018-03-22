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


class LagouspiderDownloaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):

        interview = request.meta.get('interview', '')
        if interview:
            return response

        try:
            content = json.loads(response.text)
            if content['success'] is False:
                print('返回数据不对，重新请求')
                print('返回内容', content)
                return request
        except:
            print('返回数据不对，重新请求')
            print('返回内容', response)
            return request

        if response.status == 403:
            print('连接失败，重新请求')
            return request
        return response

    def process_exception(self, request, exception, spider):
            return request

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

    def process_request(self, request, spider):
        if self.count > 30:
            self.count = 0
            self.ip_list = t.ip_list
        ip, port = random.choice(self.ip_list)
        print('new_ip: ', 'https://' + ip + ':' + port)
        request.meta['proxy'] = 'https://' + ip + ':' + port
        self.count += 1
        with open('ip_list.txt', 'a') as f:
            f.write('-----------------------------------')
            for line in self.ip_list:
                f.write(str(line))
            f.write('\n')

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)


class LagouCookiesMiddleware(object):

    # cookies = {'user_trace_token': '20180226001828-5c601f0f-6537-44be-a9c9-c1c381f97c3f',
    #            '_ga': 'GA1.2.1250218167.1519575509',
    #            'LGUID': '20180226001829-83f7b1fb-1a47-11e8-917d-525400f775ce',
    #            'index_location_city': '%E6%B7%B1%E5%9C%B3',
    #            'JSESSIONID': 'ABAAABAAAIAACBI0F6208F8F96C4F25F0401ABC9F24BABC',
    #            'hideSliderBanner20180305WithTopBannerC': '1',
    #            '_gid': 'GA1.2.2062001429.1521558973',
    #            '_gat': '1',
    #            'LGSID': '20180320231612-a050094e-2c51-11e8-914f-525400f775ce',
    #            'PRE_UTM': '',
    #            'PRE_HOST': '',
    #            'PRE_SITE': '',
    #            'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F',
    #            'LGRID': '20180320231612-a0500a4f-2c51-11e8-914f-525400f775ce',
    #            'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1520935912,1521373019,1521377635,1521558978',
    #            'TG-TRACK-CODE': 'index_search',
    #            'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1521559012',
    #            'SEARCH_ID': '6cff551f6f6c41f49b8b6bfd8357e21f'}

    cookies = [{'user_trace_token': '20180226001828-5c601f0f-6537-44be-a9c9-c1c381f97c3f',
               '_ga': 'GA1.2.1250218167.1519575509',
               'LGUID': '20180226001829-83f7b1fb-1a47-11e8-917d-525400f775ce',
               'index_location_city': '%E6%B7%B1%E5%9C%B3',
               '_gid': 'GA1.2.2062001429.1521558973',
               'hideSliderBanner20180305WithTopBannerC': '1',
               'JSESSIONID': 'ABAAABAAAIAACBI41D253C29C1CCFBCFC565C3ADACD2917',
               'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1521558978,1521598449,1521612039,1521622382',
               'TG-TRACK-CODE': 'index_navigation',
               'X_HTTP_TOKEN': '3dc49121699a69dc7f6f5deda3dcab57',
               'LGSID': '20180321221313-fe3263bc-2d11-11e8-b56c-5254005c3644',
               'PRE_UTM': '',
               'PRE_HOST': '',
               'PRE_SITE': '',
               'PRE_LAND': 'https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fmsg%3Dvalidation%26uStatus%3D2%26clientIp%3D183.53.66.197',
               'SEARCH_ID': '9c40e391eb7b4c379e4f104799c6b4ca',
               '_putrc': '04201950329B43E0',
               'login': 'true',
               'unick': '%E5%BE%90%E9%9B%84%E5%B3%B0',
               'showExpriedIndex': '1',
               'showExpriedCompanyHome': '1',
               'showExpriedMyPublish': '1',
               'hasDeliver': '8',
               'gate_login_token': 'd4ad590e51863daf7ee4b04feb97b60ba07f5fd778a2516a',
               '_gat': '1',
               'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1521642759',
               'LGRID': '20180321223239-b4e9d754-2d14-11e8-9348-525400f775ce'},
     ]

    def process_request(self, request, spider):
        request.cookies = random.choice(self.cookies)


