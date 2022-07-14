# Geoforum 这个网站使用了5s盾，所以不能用requests库，需要用cloudscraper包解决
import json
import os
import sys
import threading
import time

import cloudscraper
from lxml import etree
from retry import retry

from article import Article

sys.path.append(os.path.dirname(os.path.abspath(__file__)))    # 跳到上级目录下面（sys.path添加目录时注意是在windows还是在Linux下，windows下需要‘\\'否则会出错。）


issue_newest_article_lst = []
online_newest_article_lst = []

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }

class RequestThread(threading.Thread):
    def __init__(self, id, url, thread_lock, scraper):
        threading.Thread.__init__(self)
        self.id = id
        self.url = url
        self.headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",}
        self.thread_lock = thread_lock
        self.scraper = scraper
    
    @retry(tries=5)
    def run(self):
        try:
            response = self.scraper.get(self.url, headers=self.headers)
            self.parse_issue(response=response)
        except Exception as e:
            print(e)

    def parse_issue(self, response):
        '''Geoforum `issue`'''
        global issue_newest_article_lst
        try:
            page_text = response.text
            tree = etree.HTML(page_text)
            article_title = ''.join(tree.xpath('.//span[@class="title-text"]//text()')).strip()
            article_author = [''.join(content.xpath('.//text()')) for content in tree.xpath('.//div[@class="author-group"]/a/span[@class="content"]')]
            article_community = []
            data_json_str = ''.join(tree.xpath('.//script[@type="application/json"]//text()'))
            data_json = json.loads(data_json_str)
            for dict in data_json['authors']['content'][0]['$$']:
                if dict['#name'] == 'affiliation':
                    for sub_dict in dict['$$']:
                        if sub_dict['#name'] == 'textfn':
                            article_community.append(sub_dict['_'])


            # article_publish_date = ''.join(tree.xpath('.//div[@class="Banner"]/div[@class="wrapper"]/p//text()')).split(',')[3].replace('Available online ', '')
            article_publish_date = data_json['article']['dates']['Publication date']
            # self.thread_lock.acquire()
            issue_newest_article_lst.append((self.id, Article(article_title, article_author, article_community, article_publish_date)))
            # self.thread_lock.release()
        except Exception as e:
            print(e)
            print('解析issue返回值失败！')

def flush(progress_bar):
    global issue_newest_article_lst
    host = 'https://www.sciencedirect.com'
    site_url = "/journal/geoforum"

    scraper = cloudscraper.create_scraper()
    site_html = scraper.get(host + site_url, headers=headers, timeout=30)#503状态码
    if not site_html.status_code == 200:
        print('site_html 请求失败，状态码{}'.format(site_html.status_code))
        return False

    site_tree = etree.HTML(site_html.text)
    issue_url = site_tree.xpath('//a[@class="anchor js-volume volume-issue-text anchor-default"]')[0].get('href', '')# 注意没有href()的用法
    issue_url = host + issue_url

    # issue 更新
    issue_html = scraper.get(issue_url,headers=headers)
    if not issue_html.status_code == 200:
        print('issue_html 请求失败，状态码{}'.format(issue_html.status_code))
        return False
    
    issue_tree = etree.HTML(issue_html.text)

    newest_issue = ''.join(issue_tree.xpath('.//h2[@class="u-text-light u-h1 js-vol-issue"]/text()')).replace(' ', '_')
    print('最新issue:', newest_issue)
    
    issue_newest_article_entry = []
    issue_newest_article_entry.extend(issue_tree.xpath('.//ol[@class="article-list"]/li'))# 加点表示从当前节点以后开始搜索，不然这个节点之前的也会搜索

    progress_bar(num=30, text="获取issue文献数据……")

    # issue_queue = queue.Queue()
    issue_threads = []
    issue_thread_lock = threading.Lock()
    for id, issue_article_entry in enumerate(issue_newest_article_entry):
        article_subtype = ''.join(issue_article_entry.xpath('.//span[@class="js-article-subtype"]/text()'))
        if article_subtype and "Research article" == article_subtype:
            article_url = host + issue_article_entry.xpath('.//a[@class="anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default"]')[0].get('href', '')
            new_thread = RequestThread(id, article_url, issue_thread_lock, scraper)
            new_thread.start()
            issue_threads.append(new_thread)

    # 等待线程完成
    for t in issue_threads:
        t.join()

    progress_bar(num=60, text="解析返回数据……")

    issue_newest_article_lst = sorted(issue_newest_article_lst, key=lambda x: x[0], reverse=True)
    for id, article in issue_newest_article_lst:
        article_details = article.format()
        print(article_details)

    progress_bar(num=90, text="存入数据库")

    # 数据送入数据库
    from data_manager.data_mgr import DataManager

    try:
        database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data\\Geoforum.db')
        if not os.path.exists(database_path):
            with open(database_path, "r") as f:
                pass
            
        my_data_manager = DataManager(database_path=database_path)
        my_data_manager.create_table(newest_issue)
        for id, article in issue_newest_article_lst:
            if not my_data_manager.search_data(newest_issue, article.title):
                my_data_manager.insert_data(newest_issue, article.title, article.author, article.community, article.date)
            else:
                print(f'{article.title:<200} |已存在于 The Professional Geographer_issue')
        print('Geoforum_issue数据存储成功！')
        progress_bar(num=100, text="完成")
        time.sleep(2)
        return True

    except Exception as e:
        print(e)
        print('数据存储失败！')
        return False
    

if __name__ == "__main__":
    flush()
