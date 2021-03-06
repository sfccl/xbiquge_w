# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time
from twisted.enterprise import adbapi
from pymongo import MongoClient

class XbiqugePipeline(object):
    conn = MongoClient('mongodb://admin:admin@localhost:27017/admin')
    db = conn.novels #建立数据库novels的连接对象db
    name_novel = ''
    url_firstchapter = ''
    name_txt = ''
    start_time=time.time()

    #定义类初始化动作
    def __init__(self):

        return

    #爬虫开始
    def open_spider(self, spider):

        return

    def get_collection(self,name_collection):  #获取数据集cursor对象
        myset = self.db[name_collection]
        return myset

    def process_item(self, item, spider):
        #if self.name_novel == '':
        self.name_novel = item['name']
        self.url_firstchapter = item['url_firstchapter']
        self.name_txt = item['name_txt']
        myset = self.db[self.name_novel]
        myset.insert_one(dict(item))
#        if self.name_novel != '':
#            exec('self.db.'+ self.name_novel + '.insert_one(dict(item))')
        return item

    #从数据库取小说章节内容写入txt文件
    def content2txt(self,dbname,firsturl,txtname):
        myset = self.db[dbname]
        record_num = myset.find().count() #获取小说章节数量
        print("小说总章节数:",record_num)
        counts=record_num
        url_c = firsturl
        start_time=time.time()  #获取提取小说内容程序运行的起始时间
        f = open(txtname+".txt", mode='w', encoding='utf-8')   #写方式打开小说名称加txt组成的文件
        for i in range(counts):  #括号中为counts
#-----------使用count()方法获得的返回整型值作为是否获得数据的判断依据-------------
#            record_m_count=myset.find({"url": url_c},{"content":1,"_id":0}).count()
#            if record_m_count == 0:
#               print("数据集中没有找到章节内容。\n出错url:",url_c)
#               break
#--------------------------------------------------------------------------------

#-----------使用next()方法读取迭代器数据，并使用try except捕获未获得数据的错误-----
            try:   
                record_m=myset.find({"url": url_c},{"content":1,"_id":0}).next()
            #except Exception as e:
            except StopIteration:
                print("数据集中没有获得章节内容。\n出错url:",url_c)
                break   #跳出for循环，终止小说文件生成
#--------------------------------------------------------------------------------
            record_content_c2a0 = ''

#------------使用for循环读取迭代器数据模式---------------------------------
#            record_i = myset.find({"url": url_c},{"content":1,"_id":0})
#            for record_m in record_i:
#                record_content_c2a0 = record_m["content"]  #获取小说章节内容
#---------------------------------------------------------------------------
            record_content_c2a0 = record_m["content"] 

            #record_content=record_content_c2a0.replace(u'\xa0', u'')  #消除特殊字符\xc2\xa0
            record_content=record_content_c2a0
            #print(record_content)
            f.write('\n')
            f.write(record_content + '\n')
            f.write('\n\n')
            url_ct = myset.find({"url": url_c},{"next_page":1,"_id":0})  #获取下一章链接的查询对象
            for item_url in url_ct:
                url_c = item_url["next_page"]  #下一章链接地址赋值给url_c，准备下一次循环。
                #print("下一页",url_c)
        f.close()
        print("文件生成用时:",time.time()-start_time)
        print("小说爬取总用时:",time.time()-self.start_time)
        print(txtname + ".txt" + " 文件已生成！")
        return

    #爬虫结束，调用content2txt方法，生成txt文件
    def close_spider(self,spider):
        if self.name_novel !='' and self.url_firstchapter != '' and self.name_txt != '':
            self.content2txt(self.name_novel,self.url_firstchapter,self.name_txt)
        return

