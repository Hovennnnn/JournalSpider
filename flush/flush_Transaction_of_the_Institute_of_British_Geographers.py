# Transaction of the Institute of British Geographers (更新至Volume 47, Issue 2)
from multiprocessing.connection import wait
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, wait

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# selenium 4
from selenium.webdriver.edge.service import Service as EdgeService
from retry import retry

from flush.article import Article
from flush.edgedriver_manager import check_driver_new_version

# --------- selenium config --------------------------
if __name__ == "__main__":
    driver_path = check_driver_new_version(where="main")
else:
    driver_path = check_driver_new_version(where="import")

options = webdriver.EdgeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=1")
options.add_argument('window-size=2160x1440')
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("enable-automation")
options.add_argument('--ignore-certificate-errors')
options.add_argument('-ignore -ssl-errors')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36')# 使用无头模式得加上user-agent
options.page_load_strategy = 'eager'
prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("--headless")



issue_newest_article_lst = []
online_newest_article_lst = []

class SeleniumGet:

    def __init__(self, url, options=options, timeout=30, until_xpath=None):
        self.url = url
        self.options = options
        self.timeout = timeout
        self.until_xpath = until_xpath

    def get_html(self):
        driver = webdriver.Edge(options=self.options, service=EdgeService(driver_path))

        driver.set_page_load_timeout(time_to_wait=self.timeout)
        try:
            driver.get(self.url)
        except:
            pass
        
        if self.until_xpath:
            try:
                WebDriverWait(driver, timeout=self.timeout).until(
                    lambda x: x.find_element(By.XPATH, self.until_xpath)
                )
                return driver.page_source
            except Exception as e:
                print(self.url, "获取失败")
                print(e)
                return None



class SubCrawl():
    def __init__(self, id, url, thread_lock, options, until_xpath, parse="issue", timeout=30):
        self.id = id
        self.url = url
        self.thread_lock = thread_lock
        self.options = options
        self.until_xpath = until_xpath
        self.parse = parse
        self.timeout = timeout
    

    def run(self):
        try:
            self.html = SeleniumGet(url=self.url, options=self.options, timeout=self.timeout, until_xpath=self.until_xpath).get_html()
            if not self.html:
                raise AttributeError("获取HTML失败！")

            if self.parse == "issue":
                self.parse_issue(self.html)
            elif self.parse == "online":
                self.parse_online(self.html)
            else:
                raise ValueError("parse 参数错误！")
        except ValueError as e:
            print(e)
            raise ValueError("parse 参数错误！")
        except:
            raise AttributeError("重试解析 issue 返回值失败！请检查网络")

    def parse_issue(self, text):
        '''Transaction of the Institute of British Geographers `issue`'''
        # try:
        page_text = text
        tree = etree.HTML(page_text)
        article_title = ''.join(tree.xpath('.//div[@class="article-citation"]//h1[@class="citation__title"]//text()')).strip()
        article_author = list(set(tree.xpath('.//div[@class="loa-wrapper loa-authors hidden-xs desktop-authors"]/div[@class="accordion"]/div/div/span[@class="accordion-tabbed__tab-mobile  accordion__closed"]/a/span//text()')))
        article_community = list(set(tree.xpath('.//div[@class="loa-wrapper loa-authors hidden-xs desktop-authors"]/div[@class="accordion"]/div/div/span[@class="accordion-tabbed__tab-mobile  accordion__closed"]/div/p[2]//text()')))
        article_publish_date = ''.join(tree.xpath('.//div[@class="epub-section"]/span[@class="epub-date"]/text()'))
        if article_title and article_author and article_community and article_publish_date:
            issue_newest_article_lst.append((self.id, Article(article_title, article_author, article_community, article_publish_date)))
        else:
            print("issue 解析返回值错误", "重试")
            raise AttributeError("issue 解析返回值错误", "重试")
        # except Exception as e:
        #     print(e)
        #     print('解析issue返回值失败！')

    def parse_online(self, text):
        '''Transaction of the Institute of British Geographers `online`'''
        # try:
        page_text = text
        tree = etree.HTML(page_text)
        article_title = ''.join(tree.xpath('.//div[@class="article-citation"]//h1[@class="citation__title"]//text()')).strip()
        article_author = list(set(tree.xpath('.//div[@class="loa-wrapper loa-authors hidden-xs desktop-authors"]/div[@class="accordion"]/div/div/span[@class="accordion-tabbed__tab-mobile  accordion__closed"]/a/span//text()')))
        article_community = list(set(tree.xpath('.//div[@class="loa-wrapper loa-authors hidden-xs desktop-authors"]/div[@class="accordion"]/div/div/span[@class="accordion-tabbed__tab-mobile  accordion__closed"]/div/p[2]//text()')))
        article_publish_date = ''.join(tree.xpath('.//div[@class="epub-section"]/span[@class="epub-date"]/text()'))
        if article_title and article_author and article_community and article_publish_date:
            online_newest_article_lst.append((self.id, Article(article_title, article_author, article_community, article_publish_date)))
        else:
            print("online 解析返回值错误", "重试")
            raise AttributeError("online 解析返回值错误", "重试")

        # except Exception as e:
        #     print(e)
        #     print('解析online返回值失败！')

@retry()
def flush(progress_bar):
    global issue_newest_article_lst
    global online_newest_article_lst
    with ThreadPoolExecutor(max_workers=8) as ThreadPool:
        # sites = ["The Professional Geographer"]
        host = "https://rgs-ibg.onlinelibrary.wiley.com"
        site_url = '/journal/14755661'
        driver = webdriver.Edge(options=options, service=EdgeService(driver_path))
        driver.set_page_load_timeout(30)
        # driver.maximize_window()

        driver.get(host + site_url)

        try:
            WebDriverWait(driver, timeout=30).until(
                lambda x: x.find_element(By.XPATH, '//a[@title="Go to latest issue"]')
            )
            tmp_element = driver.find_element(By.XPATH, '//a[@title="Go to latest issue"]')
            driver.execute_script('arguments[0].click();',tmp_element)
        except Exception as e:
            print(e)
            raise RuntimeError('网页加载失败！请检查网站是否可访问')

        print("点击latest issue")


        try:
            WebDriverWait(driver, timeout=30).until(
                lambda x: x.find_element(By.XPATH, '//div[@class="issue-items-container bulkDownloadWrapper"][2]/div[@class="issue-item"]')
            )
            time.sleep(5)
        except:
            raise RuntimeError("latest issue 加载失败！")

        # issue 更新
        issue_html = driver.page_source
        issue_tree = etree.HTML(issue_html)

        newest_issue = ''.join(issue_tree.xpath('//div[@class="main-content col-md-8"]//ul[@class="rlist loc"]//div[@class="cover-image__parent-item"]//text()')).replace(',', '_').replace(' ', '_')
        print('最新issue:', newest_issue)

        progress_bar(10, "获取最新文献数据网址")

        issue_newest_article_entry = []
        issue_newest_article_entry.extend(issue_tree.xpath('.//div[@class="issue-items-container bulkDownloadWrapper"][2]/div[@class="issue-item"]'))# 加点表示从当前节点以后开始搜索，不然这个节点之前的也会搜索
        print(len(issue_newest_article_entry))

        max_page = 2
        online_urls = [host + f"/action/doSearch?SeriesKey=14755661&sortBy=Earliest&pageSize=50&startPage={page}" for page in range(max_page)]


        # online 更新
        online_newest_article_entry = []
        for online_url in online_urls:
            online_html = SeleniumGet(url=online_url, options=options, until_xpath='.//ul[@id="search-result"]').get_html()
            
            online_tree = etree.HTML(online_html)

            online_newest_article_entry.extend(online_tree.xpath('.//div[@class="item__body"]'))# 加点表示从当前节点以后开始搜索，不然这个节点之前的也会搜索

        print(len(online_newest_article_entry))

        issue_threads = []
        online_threads = []
        future_tasks = []

        @retry()
        def myrequest(id, article_url, online_threads_lock, parse="online",options=options, until_xpath='.//div[@class="article-citation"]'):
            nonlocal issue_threads
            nonlocal online_threads
            new_thread = SubCrawl(id, article_url, online_threads_lock, parse=parse,options=options, until_xpath=until_xpath)
            if parse == 'issue':
                issue_threads.append(new_thread)
            elif parse == 'online':
                online_threads.append(new_thread)
            new_thread.run()

        progress_bar(30, "获取issue文献数据……")

        issue_thread_lock = threading.Lock()
        for id, issue_article_entry in enumerate(issue_newest_article_entry):
            article_url = host + issue_article_entry.xpath('.//a[@class="issue-item__title visitable"]')[0].get('href', '')
            future = ThreadPool.submit(myrequest, id, article_url,issue_thread_lock, parse="issue",options=options, until_xpath='.//div[@class="article-citation"]')
            future_tasks.append(future)

        # 等待线程完成
        wait(future_tasks, timeout = 300)
        print("issue 请求完毕")
        future_tasks = []

        progress_bar(50, "获取online文献数据……")

        online_threads_lock = threading.Lock()
        for id, online_article_entry in enumerate(online_newest_article_entry):
            article_type = ''.join(online_article_entry.xpath('.//span[@class="meta__type"]/text()'))
            if 'ARTICLE' in article_type.upper(): # 可能会出现"Article"的情况
                article_url = host + online_article_entry.xpath('.//a[@class="publication_title visitable"]')[0].get('href', '')
                future = ThreadPool.submit(myrequest, id, article_url, online_threads_lock, parse="online",options=options, until_xpath='.//div[@class="article-citation"]')
                future_tasks.append(future)

        # 等待线程完成
        wait(future_tasks, timeout = 300)
        print("online 请求完毕")
        future_tasks = []

        progress_bar(70, "解析返回数据……")

        issue_newest_article_lst = sorted(issue_newest_article_lst, key=lambda x: x[0], reverse=True)
        for id, article in issue_newest_article_lst:
            article_details = article.format()
            print(article_details)


        print('-'*50)

        online_newest_article_lst = sorted(online_newest_article_lst, key=lambda x: x[0], reverse=True)
        for id, article in online_newest_article_lst:
            article_details = article.format()
            print(article_details)

        progress_bar(90, "存入数据库……")

        # exit(00000)
        
        # 数据送入数据库
        from flush.data_mgr import DataManager
        
        try:
            database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data\\Transaction_of_the_Institute_of_British_Geographers.db')
            if not os.path.exists(database_path):
                with open(database_path, "w"):
                    pass
                
            my_data_manager = DataManager(database_path=database_path)
            my_data_manager.create_table(newest_issue)
            for id, article in issue_newest_article_lst:
                if not my_data_manager.search_data(newest_issue, article.title):
                    my_data_manager.insert_data(newest_issue, article.title, article.author, article.community, article.date)
                else:
                    print(f'{article.title:<200} |已存在于 Transaction of the Institute of British Geographers_issue')
            print('Transaction of the Institute of British Geographers数据存储成功！')

            print('-'*200)

            my_data_manager.create_table('online')
            for id, article in online_newest_article_lst:
                if not my_data_manager.search_data('online', article.title):
                    my_data_manager.insert_data('online', article.title, article.author, article.community, article.date)
                else:
                    print(f'{article.title:<200} |已存在于 Transaction of the Institute of British Geographers_online')
            print('Transaction of the Institute of British Geographers_online数据存储成功！')
        except Exception as e:
            print(e)
            progress_bar(95, "数据存储失败……重新获取")
            raise RuntimeError('数据存储失败！')

        progress_bar(100, "完成……")
        time.sleep(2)

if __name__ == "__main__":
    flush(lambda num, text: print(f'{num}%', text))
