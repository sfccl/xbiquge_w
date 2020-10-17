# -*- coding:utf-8 -*-
#调用pipelines.py中模块HanxiangPipeline的content2txt方法，生成txt文件
from  xbiquge.pipelines import XbiqugePipeline
dbname='tsxsy_bbsgx'
firsturl='http://www.bbsgx.com/book_211549/65039517.html'
txtname='./novels/贴身小神医'
XbiqugePipeline().content2txt(dbname,firsturl,txtname)
