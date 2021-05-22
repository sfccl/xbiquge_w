# -*- coding:utf-8 -*-
#调用pipelines.py中模块HanxiangPipeline的content2txt方法，生成txt文件
from  xbiquge.pipelines import XbiqugePipeline
dbname='ss'
firsturl='https://www.xbiquge.la/49/49527/21336447.html'
txtname='./novels/绍宋'
XbiqugePipeline().content2txt(dbname,firsturl,txtname)
