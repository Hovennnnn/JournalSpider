# The Professional Geographer (更新至Volume 74, Issue 3)
import asyncio
import sys
import time

import aiohttp
import requests
from lxml import etree
from retry import retry

from article import Article

sys.path.append("..")    # 跳到上级目录下面（sys.path添加目录时注意是在windows还是在Linux下，windows下需要‘\\'否则会出错。）


issue_newest_article_lst = []
online_newest_article_lst = []

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

@retry(tries=5)
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
            if not response.status == 200:
                raise
            return page_text

def parse_issue(t):
    '''The Professional Geographer `issue`'''
    try:
        page_text = t.result()
        tree = etree.HTML(page_text)
        article_title = ''.join(tree.xpath('.//span[@class="NLM_article-title hlFld-title"]//text()')).strip()
        article_author = list(set(tree.xpath('.//span[@class="contribDegrees "]/div/a[@class="author"]/text()')))
        article_community = list(set(tree.xpath('.//span[@class="overlay"]/text()')))
        article_publish_date = ''.join(tree.xpath('.//div[@class="widget-body body body-none  body-compact-all"]/div[3]/text()')).replace('Published online: ', '')
        issue_newest_article_lst.append(Article(article_title, article_author, article_community, article_publish_date))
    except Exception as e:
        print(e)
        print('解析issue返回值失败！')

def parse_online(t):
    '''The Professional Geographer `online`'''
    try:
        page_text = t.result()
        tree = etree.HTML(page_text)
        article_title = ''.join(tree.xpath('.//span[@class="NLM_article-title hlFld-title"]//text()')).strip()
        article_author = list(set(tree.xpath('.//span[@class="contribDegrees "]/div/a[@class="author"]/text()')))
        article_community = list(set(tree.xpath('.//span[@class="overlay"]/text()')))
        article_publish_date = ''.join(tree.xpath('.//div[@class="widget-body body body-none  body-compact-all"]/div[3]/text()')).replace('Published online: ', '')
        online_newest_article_lst.append(Article(article_title, article_author, article_community, article_publish_date))
    except Exception as e:
        print(e)
        print('解析online返回值失败！')

def flush(progress_bar):
    global issue_newest_article_lst
    global online_newest_article_lst
    # sites = ["The Professional Geographer"]
    issue_urls = ["https://www.tandfonline.com/toc/rtpg20/current"]
    online_urls = ["https://www.tandfonline.com/action/showAxaArticles?journalCode=rtpg20"]

    # issue 更新
    issue_newest_article_entry = []
    for issue_url in issue_urls:
        issue_html = requests.get(issue_url,headers=headers)
        issue_tree = etree.HTML(issue_html.text)

        newest_issue = ''.join(issue_tree.xpath('//div[@class="col-md-1-6 coverCol"]//div[@class="toc-title"]/h1/text()')).replace('The Professional Geographer, ', '').replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')
        print('最新issue:', newest_issue)

        issue_newest_article_entry.extend(issue_tree.xpath('.//div[@class="tocContent"]/div[@class="articleEntry"]'))# 加点表示从当前节点以后开始搜索，不然这个节点之前的也会搜索
        nextpage = issue_tree.xpath('.//a[@class="nextPage"]')
        if nextpage:
            nextpage_href = nextpage[0].get('href', '')
            issue_urls.append('https://www.tandfonline.com' + nextpage_href) # 如果存在下一页

    # online 更新
    online_newest_article_entry = []
    for online_url in online_urls:
        online_html = requests.get(online_url,headers=headers)
        online_tree = etree.HTML(online_html.text)

        online_newest_article_entry.extend(online_tree.xpath('.//div[@class="tocContent"]/div[@class="articleEntry"]'))# 加点表示从当前节点以后开始搜索，不然这个节点之前的也会搜索
        nextpage = online_tree.xpath('.//a[@class="nextPage"]')
        if nextpage:
            nextpage_href = nextpage[0].get('href', '')
            online_urls.append('https://www.tandfonline.com' + nextpage_href) # 如果存在下一页

    progress_bar(num=30, text="获取issue文献数据……")

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    
    issue_tasks = []
    issue_article_lst_order = [] # 存下顺序
    for issue_article_entry in issue_newest_article_entry:
        if 'Article' in ''.join(issue_article_entry.xpath('.//span[@class="article-type"]/text()')):
            article_url = "https://www.tandfonline.com" + issue_article_entry.xpath('.//a[@class="ref nowrap"]')[0].get('href', '')
            issue_article_lst_order.append(''.join(issue_article_entry.xpath('.//span[@class="hlFld-Title"]//text()')))
            c = get_request(article_url)
            task = asyncio.ensure_future(c)
            task.add_done_callback(parse_issue)
            issue_tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(issue_tasks))

    progress_bar(num=50, text="获取online文献数据……")

    online_tasks = []
    online_article_lst_order = [] # 存下顺序
    for online_article_entry in online_newest_article_entry:
        if 'Article' in ''.join(online_article_entry.xpath('.//span[@class="article-type"]/text()')):
            article_url = "https://www.tandfonline.com" + online_article_entry.xpath('.//a[@class="ref nowrap"]')[0].get('href', '')
            online_article_lst_order.append(''.join(online_article_entry.xpath('.//span[@class="hlFld-Title"]//text()')))
            c = get_request(article_url)
            task = asyncio.ensure_future(c)
            task.add_done_callback(parse_online)
            online_tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(online_tasks))

    progress_bar(num=70, text="解析返回数据……")

    issue_newest_article_lst = sorted(issue_newest_article_lst, key=lambda x: issue_article_lst_order.index(x.title), reverse=True)
    for article in issue_newest_article_lst:
        article_details = article.format()
        print(article_details)


    print('-'*50)
    online_newest_article_lst = sorted(online_newest_article_lst, key=lambda x: online_article_lst_order.index(x.title), reverse=True)
    for article in online_newest_article_lst:
        article_details = article.format()
        print(article_details)

    progress_bar(num=90, text="存入数据库……")

    # 数据送入数据库
    from data_manager.data_mgr import DataManager
    import os
    try:
        database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data\\The_Professional_Geographer.db')
        if not os.path.exists(database_path):
            with open(database_path, "r") as f:
                pass
        
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

    progress_bar(num=100, text="完成")
    time.sleep(2)

if __name__ == "__main__":
    flush()