# Geoforum 这个网站使
# 用了5s盾，所以不能用requests库，需要用cloudscraper包解决
# from multiprocessing.connection import wait
import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait

import cloudscraper
from lxml import etree
from retry import retry

from flush.article import Article


issue_newest_article_lst = []
online_newest_article_lst = []

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }

class RequestThread():
    def __init__(self, scraper, id, url, parse):
        self.scraper = scraper
        self.id = id
        self.url = url
        self.headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",}
        self.parse = parse
    
    def run(self):
        try:
            response = self.scraper.get(self.url, headers=self.headers)
            if self.parse == "issue":
                self.parse_issue(response=response)
            elif self.parse == "online":
                self.parse_online(response=response)
            else:
                raise RuntimeError("parse 参数错误")
        except Exception as e:
            print(e, self.url)
            raise RuntimeError("多线程爬虫出错！", self.url)

    def parse_issue(self, response):
        '''Geoforum `issue`'''
        global issue_newest_article_lst
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
                    if sub_dict['#name'] == 'textfn' and sub_dict.get('_', None):
                        article_community.append(sub_dict['_'])
                        break
                    elif sub_dict['#name'] == 'source-text'and sub_dict.get('_', None):
                        article_community.append(sub_dict['_'])
                        break


        # article_publish_date = ''.join(tree.xpath('.//div[@class="Banner"]/div[@class="wrapper"]/p//text()')).split(',')[3].replace('Available online ', '')
        article_publish_date = data_json['article']['dates']['Publication date']
        # self.thread_lock.acquire()
        issue_newest_article_lst.append((self.id, Article(article_title, article_author, article_community, article_publish_date)))
        # self.thread_lock.release()
        # except Exception as e:
        #     print(e)
        #     print('解析issue返回值失败！')
    
    def parse_online(self, response):
        '''Geoforum `online`'''
        global online_newest_article_lst
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
                    if sub_dict['#name'] == 'textfn' and sub_dict.get('_', None):
                        article_community.append(sub_dict['_'])
                        break
                    elif sub_dict['#name'] == 'source-text'and sub_dict.get('_', None):
                        article_community.append(sub_dict['_'])
                        break
                    # else:
                    #     raise RuntimeError("解析网页数据错误！")

        # article_publish_date = ''.join(tree.xpath('.//div[@class="Banner"]/div[@class="wrapper"]/p//text()')).split(',')[3].replace('Available online ', '')
        article_publish_date = data_json['article']['dates']['Publication date']
        # self.thread_lock.acquire()
        online_newest_article_lst.append((self.id, Article(article_title, article_author, article_community, article_publish_date)))
        # self.thread_lock.release()
        # except Exception as e:
        #     print(e)
        #     print('解析online返回值失败！')

@retry()
def flush(progress_bar):
    global issue_newest_article_lst
    global online_newest_article_lst
    with ThreadPoolExecutor(max_workers=8) as ThreadPool:
        host = 'https://www.sciencedirect.com'
        site_url = "/journal/geoforum"

        scraper = cloudscraper.create_scraper()
        site_html = scraper.get(host + site_url, headers=headers, timeout=30)#503状态码
        if not site_html.status_code == 200:
            raise RuntimeError('site_html 请求失败，状态码{}'.format(site_html.status_code))

        site_tree = etree.HTML(site_html.text)
        issue_url = site_tree.xpath('//a[@class="anchor js-volume volume-issue-text anchor-default"]')[0].get('href', '')# 注意没有href()的用法
        issue_url = host + issue_url
        # issue_url = 'https://www.sciencedirect.com/journal/geoforum/vol/134/suppl/C'

        # issue 更新
        issue_html = scraper.get(issue_url,headers=headers)
        if not issue_html.status_code == 200:
            raise RuntimeError('issue_html 请求失败，状态码{}'.format(issue_html.status_code))
        
        issue_tree = etree.HTML(issue_html.text)

        newest_issue = ''.join(issue_tree.xpath('.//h2[@class="u-text-light u-h1 js-vol-issue"]/text()')).replace(' ', '_')
        print('最新issue:', newest_issue)
        
        issue_newest_article_entry = []
        issue_newest_article_entry.extend(issue_tree.xpath('.//ol[@class="article-list"]/li'))# 加点表示从当前节点以后开始搜索，不然这个节点之前的也会搜索

        progress_bar(30, "获取issue文献数据……")

        issue_threads = []
        online_threads = []
        future_tasks = []

        @retry(tries=10)
        def myrequest(scraper, id, article_url, parse="online"):
            nonlocal issue_threads
            nonlocal online_threads
            new_thread = RequestThread(scraper, id, article_url, parse=parse)
            if parse == 'issue':
                issue_threads.append(new_thread)
            elif parse == 'online':
                online_threads.append(new_thread)
            new_thread.run()
        

        for id, issue_article_entry in enumerate(issue_newest_article_entry):
            article_subtype = ''.join(issue_article_entry.xpath('.//span[@class="js-article-subtype"]/text()'))
            if article_subtype and "Research article" == article_subtype:
                article_url = host + issue_article_entry.xpath('.//a[@class="anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default"]')[0].get('href', '')
                future = ThreadPool.submit(myrequest, scraper=scraper, id=id, article_url=article_url, parse="issue")
                future_tasks.append(future)

        # online 更新
        progress_bar(50, "获取Articles in press文献数据……")

        online_newest_article_entry = []
        online_url = "https://www.sciencedirect.com/journal/geoforum/articles-in-press?page={}"

        online_html = scraper.get(online_url.format(1))
        if not online_html.status_code == 200:
            raise RuntimeError('online_html 请求失败，状态码{}'.format(online_html.status_code))

        online_tree = etree.HTML(online_html.text)
        pages_label = online_tree.xpath('.//span[@class="pagination-pages-label u-margin-s-left-from-sm u-margin-s-right-from-sm"]//text()')
        if pages_label and len(pages_label) == 4:
            pages_num = int(pages_label[3])
            print(f"Articles in press: 共{pages_num}页")
        online_urls = [online_url.format(i + 1) for i in range(pages_num)]
        for online_url in online_urls:
            online_html = scraper.get(online_url)
            online_tree = etree.HTML(online_html.text)
            online_newest_article_entry.extend(online_tree.xpath('.//ol[@class="js-article-list article-list-items"]/li'))# 加点表示从当前节点以后开始搜索，不然这个节点之前的也会搜索


        for id, online_article_entry in enumerate(online_newest_article_entry):
            article_subtype = ''.join(online_article_entry.xpath('.//span[@class="js-article-subtype"]/text()'))
            if article_subtype and "Research article" == article_subtype:
                article_url = host + online_article_entry.xpath('.//a[@class="anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default"]')[0].get('href', '')
                future = ThreadPool.submit(myrequest, scraper=scraper, id=id, article_url=article_url, parse="online")
                future_tasks.append(future)

        # 等待线程完成
        wait(future_tasks, timeout = 300)
        print("issue和online请求完毕")
        
        print(f"issue num: {len(issue_threads)}")
        print(f"online num: {len(online_threads)}")
        print(f"总线程{len(future_tasks)}")
        # future_tasks = []

        progress_bar(80, "解析返回数据……")

        issue_newest_article_lst = sorted(issue_newest_article_lst, key=lambda x: x[0], reverse=True)
        for id, article in issue_newest_article_lst:
            article_details = article.format()
            print(article_details)

        online_newest_article_lst = sorted(online_newest_article_lst, key=lambda x: x[0], reverse=True)
        for id, article in online_newest_article_lst:
            article_details = article.format()
            print(article_details)

        progress_bar(90, "存入数据库")

        # 数据送入数据库
        from flush.data_mgr import DataManager

        try:
            database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data\\Geoforum.db')
            if not os.path.exists(database_path):
                with open(database_path, "w"):
                    pass
                
            my_data_manager = DataManager(database_path=database_path)
    
            my_data_manager.create_table(newest_issue)
            for id, article in issue_newest_article_lst:
                if not my_data_manager.search_data(newest_issue, article.title):
                    my_data_manager.insert_data(newest_issue, article.title, article.author, article.community, article.date)
                else:
                    print(f'{article.title:<200} |已存在于 The Professional Geographer_issue')
            
            my_data_manager.create_table("online")
            for id, article in online_newest_article_lst:
                if not my_data_manager.search_data("online", article.title):
                    my_data_manager.insert_data("online", article.title, article.author, article.community, article.date)
                else:
                    print(f'{article.title:<200} |已存在于 The Professional Geographer_online')

            print('Geoforum_issue数据存储成功！')
            progress_bar(100, "完成")
            time.sleep(2)
            return True

        except Exception as e:
            print(e)
            print('数据存储失败！')
            return False
    

if __name__ == "__main__":
    flush(lambda num, text: print(num, text))
