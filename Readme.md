网站
(综合顶刊) Annals of the Association of American Geographers (更新至 Volume 112, Issue 5)
https://www.tandfonline.com/journals/raag21
(综合期刊、短小文章、教育) The Professional Geographer (Volume 74, Issue 3)
https://www.tandfonline.com/journals/rtpg20
(自然生态) Geoforum (更新至 volume 133)
https://www.sciencedirect.com/journal/geoforum
(综合顶刊) Transaction of the Institute of British Geographers (更新至 Volume 47, Issue 2)
https://rgs-ibg.onlinelibrary.wiley.com/journal/14755661
(综合期刊、短小文章) The Geographical Journal (更新至 Volume 188, Issue 2)
https://rgs-ibg.onlinelibrary.wiley.com/journal/14754959

---

https://www.sciencedirect.com/journal/geoforum：
5s 盾、br 格式传输会出现解码乱码(使用 brotli 库)
数据存在`<script type="application/json">`中，是 json 格式

---

Transaction of the Institute of British Geographers 
https://rgs-ibg.onlinelibrary.wiley.com/journal/14755661:

也使用 5s 盾：
第一次请求返回状态码 503，response 的 cookie 有`_cf_bm`字段，Miscellaneous 有`CF-RAY`字段

第二次请求：
参数`ray`来自`CF-RAY`字段‘-’之前的部分，
第二次请求的 cookie 包含`_cf_bm`，
第二次请求的 Referer 中的参数`__cf_chl_rt_tk`来自第一次请求的 js

第二次请求的返回值是一段 js

第三次请求：
参数`ray`同第二次请求
cookie仍是`__cf_bm`
请求结果是个gif，返回值有个新的`CF_RAY`

第四次请求：
参数`ray`同第二次请求
cookie仍是`__cf_bm`
请求结果是个gif，返回值也有个新的`CF_RAY`

第五次请求：
请求cookie包含`__cf_bm`、`cf_chl_2`和`cf_chl_prog`，其中`cf_chl_2`来自第一次请求的html的一段js的`cHash`中，`cf_chl_prog`来自第二次请求的js（例子中是e）

响应包含`set-cookie`字段`cf_chl_seq_{cf_chl_2}`

第六次请求：
请求cookie有四个参数，分别是`cf_chl_seq_389774c89d4a6a2`、
	`__cf_bm`、
	`cf_chl_2`、
	`cf_chl_prog`（注意这里和前面值不同）

响应



§ State Key Laboratory of Resources and Environmental Information System, Institute of Geographic Sciences and Natural Resources Research, CAS, China; 
* State Key Laboratory of Resources and Environmental Information System, Institute of Geographic Sciences and Natural Resources Research, CAS, China, and College of Resources and Environment, University of Chinese Academy of Sciences, China; 
† State Key Laboratory of Resources and Environmental Information System, Institute of Geographic Sciences and Natural Resources Research, CAS, China, and College of Resources and Environment, University of Chinese Academy of Sciences, China, and Jiangsu Center for Collaborative Innovation in Geographical Information Resource Development and Application and School of Geography, Nanjing Normal University, China; 
‡ State Key Laboratory of Resources and Environmental Information System, Institute of Geographic Sciences and Natural Resources Research, CAS, China, Jiangsu Center for Collaborative Innovation in Geographical Information Resource Development and Application and School of Geography, Nanjing Normal University, China, and Department of Geography, University of Wisconsin–Madison, USA