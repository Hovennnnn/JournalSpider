# JournalSpider

This repository is a spider for some Journal site.

---

## site：

- (综合顶刊) Annals of the Association of American Geographers (更新至 Volume 112, Issue 5)
  - https://www.tandfonline.com/journals/raag21
- (综合期刊、短小文章、教育) The Professional Geographer (Volume 74, Issue 3)
  - https://www.tandfonline.com/journals/rtpg20
- (自然生态) Geoforum (更新至 volume 133)
  - https://www.sciencedirect.com/journal/geoforum
- (综合顶刊) Transaction of the Institute of British Geographers (更新至 Volume 47, Issue 2)
  - https://rgs-ibg.onlinelibrary.wiley.com/journal/14755661
- (综合期刊、短小文章) The Geographical Journal (更新至 Volume 188, Issue 2)
  - https://rgs-ibg.onlinelibrary.wiley.com/journal/14754959

---

## 关于 cloudflare5s 盾的处理方法：

- https://www.sciencedirect.com/journal/geoforum：
  - 使用 cloud_scraper 库解决

---

- Transaction of the Institute of British Geographers (https://rgs-ibg.onlinelibrary.wiley.com/journal/14755661):
- The Geographical Journal (https://rgs-ibg.onlinelibrary.wiley.com/journal/14754959):

  - 这两个网站用 cloud_scraper 解决不了，使用 selenium + 多线程代替，速度慢了一些。

    - 找遍全网很少找到相关的方法，分析了一波又懒得一个个请求去写，就把分析的一点结果放上来吧，有遗漏的还请海涵：

          抓包获取这两个网站5s盾的流程：

          第一次请求返回状态码 503，response 的 cookie 有`_cf_bm`字段，Miscellaneous 有`CF-RAY`字段

          第二次请求：
          参数`ray`来自`CF-RAY`字段‘-’之前的部分，
          第二次请求的 cookie 包含`_cf_bm`，
          第二次请求的 Referer 中的参数`__cf_chl_rt_tk`来自第一次请求的 js

          第二次请求的返回值是一段 js

          第三次请求：
          参数`ray`同第二次请求
          cookie 仍是`__cf_bm`
          请求结果是个 gif，返回值有个新的`CF_RAY`

          第四次请求：
          参数`ray`同第二次请求
          cookie 仍是`__cf_bm`
          请求结果是个 gif，返回值也有个新的`CF_RAY`

          第五次请求：
          请求 cookie 包含`__cf_bm`、`cf_chl_2`和`cf_chl_prog`，其中`cf_chl_2`来自第一次请求的 html 的一段 js 的`cHash`中，`cf_chl_prog`来自第二次请求的 js（例子中是 e）

          响应包含`set-cookie`字段`cf_chl_seq_{cf_chl_2}`

          第六次请求：
          请求 cookie 有四个参数，分别是`cf_chl_seq_389774c89d4a6a2`、
          `__cf_bm`、
          `cf_chl_2`、
          `cf_chl_prog`（注意这里和前面值不同）

      - 参考文章：
        - https://cloud.tencent.com/developer/article/2014604
        - https://mp.weixin.qq.com/s/efloBirboVfH2hK3cNoU5A
