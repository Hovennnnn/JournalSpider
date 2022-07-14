# Transaction of the Institute of British Geographers (更新至Volume 47, Issue 2)
import asyncio
import sys

import aiohttp
import requests
from lxml import etree

from article import Article

sys.path.append("..")    # 跳到上级目录下面（sys.path添加目录时注意是在windows还是在Linux下，windows下需要‘\\'否则会出错。）


issue_newest_article_lst = []
online_newest_article_lst = []

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

async def get_request(url):
    # 实例化好了一个请求对象
    async with aiohttp.ClientSession() as sess:
        # 调用get发起请求，返回一个响应对象
        # get/post(url, headers, params/data, proxy='')
        async with await sess.get(url=url, headers=headers) as response:
            # text()获取字符串形式的响应数据
            # read()获取byte类型的响应数据
            # json()获取字典类型的响应数据
            page_text = await response.text()
            return page_text

def parse_issue(t):
    '''Transaction of the Institute of British Geographers `issue`'''
    try:
        page_text = t.result()
        tree = etree.HTML(page_text)
        article_title = ''.join(tree.xpath('.//div[@class="article-citation"]//h1[@class="citation__title"]//text()')).strip()
        article_author = list(set(tree.xpath('.//div[@class="loa-wrapper loa-authors hidden-xs desktop-authors"]/div[@class="accordion"]/div/div/span[@class="accordion-tabbed__tab-mobile  accordion__closed"]/a/span//text()')))
        article_community = list(set(tree.xpath('.//div[@class="loa-wrapper loa-authors hidden-xs desktop-authors"]/div[@class="accordion"]/div/div/span[@class="accordion-tabbed__tab-mobile  accordion__closed"]/div/p[2]//text()')))
        article_publish_date = ''.join(tree.xpath('.//div[@class="epub-section/span[@class="epub-date"]/text()'))
        issue_newest_article_lst.append(Article(article_title, article_author, article_community, article_publish_date))
    except Exception as e:
        print(e)
        print('解析issue返回值失败！')

def parse_online(t):
    '''Transaction of the Institute of British Geographers `online`'''
    try:
        page_text = t.result()
        tree = etree.HTML(page_text)
        article_title = ''.join(tree.xpath('.//span[@class="NLM_article-title hlFld-title"]//text()')).strip()
        article_author = list(set(tree.xpath('.//span[@class="contribDegrees "]/div/a[@class="author"]/text()')))
        article_community = tree.xpath('.//span[@class="overlay"]/text()')
        article_publish_date = ''.join(tree.xpath('.//div[@class="widget-body body body-none  body-compact-all"]/div[3]/text()')).replace('Published online: ', '')
        online_newest_article_lst.append(Article(article_title, article_author, article_community, article_publish_date))
    except Exception as e:
        print(e)
        print('解析online返回值失败！')


def flush():
    # sites = ["The Professional Geographer"]
    host = "https://rgs-ibg.onlinelibrary.wiley.com"
    site_url = '/journal/14755661'
    site_html = requests.get(host + site_url)
    if not site_html.status_code == 200:
        print('site_html 请求失败，状态码{}'.format(site_html.status_code))
        return False

    try:
        site_tree = etree.HTML(site_html.text)
        issue_url = site_tree.xpath('//a[@title="Go to latest issue"]')[0].get('href', '')# 注意没有href()的用法
        issue_url = host + issue_url
    except Exception as e:
        print(e)
        print('latest issue-url don\'t exist!')
        return False

    max_page = 10
    online_urls = [host + "/action/doSearch?SeriesKey=14755661&sortBy=Earliest&pageSize=100&startPage={page}" for page in range(max_page)]

    # issue 更新
    issue_html = requests.get(issue_url,headers=headers)
    if not issue_html.status_code == 200:
        print("issue_html 请求失败，状态码{}".format(issue_html.status_code))
        return False

    issue_tree = etree.HTML(issue_html.text)

    newest_issue = ''.join(issue_tree.xpath('//div[@class="main-content col-md-8"]//ul[@class="rlist loc"]//div[@class="cover-image__parent-item"]//text()')).replace(',', '_').replace(' ', '_')
    print('最新issue:', newest_issue)

    issue_newest_article_entry = []
    issue_newest_article_entry.extend(issue_tree.xpath('.//div[@class="issue-item"]'))# 加点表示从当前节点以后开始搜索，不然这个节点之前的也会搜索

    # online 更新
    online_newest_article_entry = []
    for online_url in online_urls:
        online_html = requests.get(online_url,headers=headers)
        if not online_html.status_code == 200:
            print('online_html 请求失败，状态码{}'.format(online_html.status_code))
            return False
        
        online_tree = etree.HTML(online_html.text)

        online_newest_article_entry.extend(online_tree.xpath('.//div[@class="item__body"]'))# 加点表示从当前节点以后开始搜索，不然这个节点之前的也会搜索
        

    issue_tasks = []
    issue_article_lst_order = [] # 存下顺序
    for issue_article_entry in issue_newest_article_entry:
        article_url = host + issue_article_entry.xpath('.//a[@class="issue-item__title visitable"]')[0].get('href', '')
        issue_article_lst_order.append(''.join(issue_article_entry.xpath('.//a[@class="issue-item__title visitable"]/h2//text()')))
        c = get_request(article_url)
        task = asyncio.ensure_future(c)
        task.add_done_callback(parse_issue)
        issue_tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(issue_tasks))


    online_tasks = []
    online_article_lst_order = [] # 存下顺序
    for online_article_entry in online_newest_article_entry:
        if 'ARTICLE' in ''.join(online_article_entry.xpath('.//span[@class="meta__type"]/text()')):
            article_url = host + online_article_entry.xpath('.//a[@class="publication_title visitable"]')[0].get('href', '')
            online_article_lst_order.append(''.join(online_article_entry.xpath('.//a[@class="publication_title visitable"]//text()')))
            c = get_request(article_url)
            task = asyncio.ensure_future(c)
            task.add_done_callback(parse_online)
            online_tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(online_tasks))

    issue_newest_article_lst = sorted(issue_newest_article_lst, key=lambda x: issue_article_lst_order.index(x.title), reverse=True)
    for article in issue_newest_article_lst:
        article_details = article.format()
        print(article_details)


    print('-'*50)
    online_newest_article_lst = sorted(online_newest_article_lst, key=lambda x: online_article_lst_order.index(x.title), reverse=True)
    for article in online_newest_article_lst:
        article_details = article.format()
        print(article_details)



    # 数据送入数据库
    from data_manager.data_mgr import DataManager

    try:
        database_path = '..\\data\\Transaction_of_the_Institute_of_British_Geographers.db'
        my_data_manager = DataManager(database_path=database_path)
        my_data_manager.create_table(newest_issue)
        for article in issue_newest_article_lst:
            if not my_data_manager.search_data(newest_issue, article.title):
                my_data_manager.insert_data(newest_issue, article.title, article.author, article.community, article.date)
            else:
                print(f'{article.title:<200} |已存在于 The Professional Geographer_issue')
        print('The Professional Geographer_issue数据存储成功！')

        print('-'*200)

        my_data_manager.create_table('online')
        for article in online_newest_article_lst:
            if not my_data_manager.search_data('online', article.title):
                my_data_manager.insert_data('online', article.title, article.author, article.community, article.date)
            else:
                print(f'{article.title:<200} |已存在于 The Professional Geographer_online')
        print('The Professional Geographer_online数据存储成功！')
    except Exception as e:
        print(e)
        print('数据存储失败！')

if __name__ == "__main__":
    flush()