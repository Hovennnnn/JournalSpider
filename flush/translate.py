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

import random
import time
from hashlib import md5
import requests
from googletrans import Translator

class YoudaoSpider:

    def __init__(self, word):
        # url一定要写抓包时抓到的POST请求的提交地址，但是还需要去掉 url中的'_o'，
        # '_o'这是一种url反爬策略，做了页面跳转，若直接访问会返回{"errorCode":50}
        self.url = 'https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        }
        self.word = word

    # 获取lts时间戳,salt加密盐,sign加密签名
    def get_lts_salt_sign(self, word):
        lts = str(int(time.time() * 10000))
        salt = lts + str(random.randint(0, 9))
        string = "fanyideskweb" + word + salt + "Ygy_4c=r#e#4EX^NUGUc5"
        s = md5()
        # md5的加密串必须为字节码
        s.update(string.encode())
        # 16进制加密
        sign = s.hexdigest()
        # print(lts, salt, sign)
        return lts, salt, sign

    def attack_yd(self, word):
        lts, salt, sign = self.get_lts_salt_sign(word)
        # 构建form表单数据
        data = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'lts': lts,
            'bv': 'bdc0570a34c12469d01bfac66273680d',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
        }
        # 使用 reqeusts.post()方法提交请求
        resp = requests.post(self.url, headers=self.headers, data=data)
        # 将json格式的字符串转为python数据类型
        html = resp.json()
        # print(html)
        # {"translateResult":[[{"tgt":"你好世界","src":"hello world"}]]}
        res = html['translateResult'][0][0]['tgt']
        # print('翻译结果：', res)
        return res

    def translate(self):
        try:
            return self.attack_yd(self.word)
        except Exception as e:
            print(e)


class GoogleSpider(Translator):

    def __init__(self, word):
        super().__init__(
            service_urls=["translate.google.cn"]
        )                                        # 如果可以上外网，还可添加 'translate.google.com' 等
        self.word = word

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
    spider = YoudaoSpider("youdao")
    print(spider.translate())
    spider1 = GoogleSpider("google")
    print(spider1.translate())