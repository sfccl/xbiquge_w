# -*- coding:utf-8 -*-
#调用pipelines.py中模块HanxiangPipeline的content2txt方法，生成txt文件
import sys
from  xbiquge.pipelines import XbiqugePipeline
dbname='wdssny'
firsturl='https://www.xbiquge.la/80/80058/31226099.html'
txtname='./novels/我的杀手女友'
url_chapters = firsturl[0:32]
#XbiqugePipeline().content2txt(dbname,firsturl,txtname)
myset=XbiqugePipeline().get_collection(dbname)
url_counts=myset.find({"url":url_chapters},{"url":1,"_id":0,"next_page":1}).count()
print(url_counts)
#print(obj_url)
#print(obj_url.hasNext())
#if obj_url.next() != '' :
#try:
#    print("对象内容：",obj_url.next())
#except StopIteration:
#    print("数据集中没有找到数据")


