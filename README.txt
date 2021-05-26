小说抓取说明：

一、正常抓取
1、拷贝爬虫模板文件xbiquge/spiders/sancun.py
若在xbiquge网站中，只需要修改爬虫名（name），章节目录url（start_urls），第一章url（url_firstchapter），小说中文名（name_txt）等参数即可
2、xbiquge/pipelines.py文件一般不用修改，若是发生错误，可取消该文件中的一些print语句以跟踪出错信息。
3、xbiquge/settings.py文件一般不用修改，若抓取过程中出现异常，可修改一些参数，如DOWNLOAD_DELAY参数可设为2或3等等。
4、若是其他网站，则需要通过测试，修改对应的items条目内容，具体情况具体分析。
5、xbiquge_w是使用mongodb作为小说存储数据库。
6、myspiders.log是爬虫log文件，记录抓取过程，该文件可用于排错。
7、spider2txt.py是单独生成小说txt文件的程序，需要修改其中的变量。运行方法：python spider2txt.py

二、抓取单章方法
有时，在抓取小说过程中，会出现个别章节没有成功抓取，若重新全部抓取的话比较费时，考虑抓取单章内容进行补充。
1、修改爬虫文件，模板：xiaoyaoxss1.py （取消爬取目录页的parse函数，直接爬取单页内容）
2、修改pipelines.py, 模板: pipelines1.py  (取消爬虫起始函数，避免重新建表损坏数据表已有内容。注意，pipelines1.py需要修改为pipelines.py才可用。单章抓取完成后，应及时恢复原pipelines.py文件。)
3、运行单章爬取爬虫： scrapy crawl xiaoyaoxss1.py
4、若内容补充完成，需要重新生成txt文件，直接运行spiders2txt.py即可：python spiders2txt.py

三、2021年5月26日修改
1、本次修改xbiquge/pipelines.py和xbiquge/spiders/sancun.py文件，使爬取过程中不用清空数据集（collection），若一次爬取不成功，可继续多次爬取。
2、爬取过程中最可能的因素是爬取的网页错误导致无法输出正确的小说txt文件，要注意检查小说数据集内容，有必要的话，可登录mongodb数据，使用db.sancun.remove({})命令清空数据集后，再次爬取。


