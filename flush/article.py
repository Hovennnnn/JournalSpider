from translate import YoudaoSpider, GoogleSpider
import json

class Article:
    def __init__(self, title, author, community, date, url='', journal='Annals of the American Association of Geographers'):
        self.title = title
        self.chinese_title = GoogleSpider(self.title).translate()
        if type(author) == type("string"):
            self.author = author
        else:
            self.author = '，'.join(author) # 注意这里是列表
        if type(community) == type("string"):
            self.community = community
        else:
            self.community = '; '.join(community)# 注意这里是列表

        self.date = date
        self.url = url
        self.journal = journal

    def format(self):
        return f"{self.title}\n{self.chinese_title}\n作者：{self.author}\n单位：{self.community}\n发表日期：{self.date}\n\n"

    def to_dict(self):
        '''
        return the data in terms of dict
        '''
        return {'title': self.title, 'author': self.author, 'community': self.community, 'author': self.author, 'date': self.date, 'url': self.url}

    def to_json(self):
        '''
        return the data in terms of json string
        '''
        return json.dumps(self.to_dict())

if __name__ == "__main__":
    article = Article(1, 2, 3, 4, '000')
    js = article.to_json()
    with open('data/test.json', 'w', encoding="utf-8") as f:
        f.write(js)
