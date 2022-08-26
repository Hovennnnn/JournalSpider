'''
JS加密代码
var r = function(e) {
        var t = n.md5(navigator.appVersion)
          , r = "" + (new Date).getTime()
          , i = r + parseInt(10 * Math.random(), 10);
        return {
            ts: r,
            bv: t,
            salt: i,
            sign: n.md5("fanyideskweb" + e + i + "Ygy_4c=r#e#4EX^NUGUc5")
        }
    };
r = lts   i = salt  e = word
'''

# import time
# print(int(time.time())*10000)
# '16549975400000'  python输出
# '16549969865516'  有道 lts
# 'sign: ca53ec0dbad1d3ad020fcfabc86f0387' 32位

import hashlib
import json
import random
import time

import requests
from retry import retry
from func_timeout import func_set_timeout, FunctionTimedOut
from googletrans import Translator


class YoudaoSpider:


    def __init__(self, msg):
        self.msg = msg

    @func_set_timeout(5)
    def translate(self):
        """修改简化之后"""
        url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        youdao_salt = "Ygy_4c=r#e#4EX^NUGUc5"
        time_salt = str(int(time.time() * 1000) + random.randint(0, 10))
        sign_ori = "fanyideskweb" + self.msg + time_salt + youdao_salt
        sign_hash = hashlib.md5(sign_ori.encode('utf-8')).hexdigest()
        headers = {
            'Referer': 'https://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }
        cookies = {
            'OUTFOX_SEARCH_USER_ID':"-193797189@10.105.137.204",
            'OUTFOX_SEARCH_USER_ID_NCOO':"67845192.25349042",
            '___rl__test__cookies': "1661481649264"
        }
        data = {
            'i': self.msg,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': time_salt,
            'sign': sign_hash,
            'doctype': 'json',
            'version': '3.0',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION',
            'typoResult': 'true'
        }
        res_json = requests.post(url, data=data, headers=headers).json()
        return res_json["translateResult"][0]



class GoogleSpider(Translator):

    def __init__(self, word):
        super().__init__(
            service_urls=["translate.google.cn"]
        )                                        # 如果可以上外网，还可添加 'translate.google.com' 等
        self.word = word

    @retry(exceptions=FunctionTimedOut, tries=3, delay=2, backoff=2, max_delay=8)
    @func_set_timeout(5)
    def translate(self):
        trans = super().translate(
            self.word, src='auto', dest='zh-cn'
        )
        # # 原文
        # print(trans.origin)
        # # 译文
        # print(trans.text)
        return trans.text


if __name__ == '__main__':
    # spider = YoudaoSpider("youdao")
    # print(spider.translate())
    spider1 = GoogleSpider("google")
    print(spider1.translate())
