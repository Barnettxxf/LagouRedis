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
    user_trace_token=20180226001828-5c601f0f-6537-44be-a9c9-c1c381f97c3f; _ga=GA1.2.1250218167.1519575509; LGUID=20180226001829-83f7b1fb-1a47-11e8-917d-525400f775ce; index_location_city=%E6%B7%B1%E5%9C%B3; _gid=GA1.2.2062001429.1521558973; JSESSIONID=ABAAABAAAIAACBI41D253C29C1CCFBCFC565C3ADACD2917; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521558978,1521598449,1521612039,1521622382; TG-TRACK-CODE=index_navigation; X_HTTP_TOKEN=3dc49121699a69dc7f6f5deda3dcab57; _putrc=04201950329B43E0; login=true; unick=%E5%BE%90%E9%9B%84%E5%B3%B0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=8; LGSID=20180322103511-a4a7c2cf-2d79-11e8-93d2-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F4300762.html; gate_login_token=60ffb4152e17a579c27d56ddc884393be7b0c1469ada87b4; _gat=1; LGRID=20180322105527-79a702d4-2d7c-11e8-93d4-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521687329; SEARCH_ID=33f0383ad5e248c496e84f740eea987f
    """
    print(format_cookies(cookies))
    #
    # city = '%E6%B7%B1%E5%9C%B3'
    # print(unquote_city(city))