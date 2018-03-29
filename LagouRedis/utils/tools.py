# -*- coding:utf-8 -*-

from urllib.parse import unquote


def format_cookies(cookie_str):
    cookie_list = cookie_str.split(';')
    container = {}
    for cookie in cookie_list:
        key = cookie.split('=')[0].strip()
        value = cookie.split('=')[1].strip()
        container[key] = value

    print('cookies length:', len(container))
    return container


def unquote_city(string, encoding=None):
    return unquote(string, encoding=encoding)


if __name__ == '__main__':
    cookies = """
    user_trace_token=20180226001828-5c601f0f-6537-44be-a9c9-c1c381f97c3f; _ga=GA1.2.1250218167.1519575509; LGUID=20180226001829-83f7b1fb-1a47-11e8-917d-525400f775ce; index_location_city=%E6%B7%B1%E5%9C%B3; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; _gid=GA1.2.1435031256.1522222631; JSESSIONID=ABAAABAAAFCAAEGB429AD4B0896694101694DC8B742D243; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522032656,1522222631,1522228134,1522234524; LGSID=20180328230149-f1306dc2-3298-11e8-a303-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; X_HTTP_TOKEN=3dc49121699a69dc7f6f5deda3dcab57; gate_login_token=""; ab_test_random_num=0; hasDeliver=0; _gat=1; SEARCH_ID=70da247715664d05add308a49cdf868f; TG-TRACK-CODE=search_code; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522250309; LGRID=20180328231828-44905e89-329b-11e8-b653-5254005c3644; LG_LOGIN_USER_ID=c410d048602b2ea504ead9df3fbaa3a59dea13b8882bcdf22c5a7a4bc7aee16b; _putrc=9E88F39614962A68123F89F2B170EADC; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B73159; gate_login_token=7a76cd53defdb8f5b007490594eddb2cb2ecb87577608fd26ee0ffabf3c2e19c
    """
    print(format_cookies(cookies))

    city = '%E6%B7%B1%E5%9C%B3'
    print(unquote_city(city))