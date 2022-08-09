# -*- coding: utf-8 -*-
import scrapy
from xbiquge.items import XbiqugeItem
from xbiquge.pipelines import XbiqugePipeline
import pdb

class SancunSpider(scrapy.Spider):
    name = 'tfwdhksd'
    allowed_domains = ['www.xbiquge.la']
    #start_urls = ['https://www.xbiquge.la/10/10489/']
    url_ori= "https://www.xbiquge.la"
    url_firstchapter = "https://www.xbiquge.la/58/58834/24307689.html"
    name_txt = "./novels/腾飞我的航空时代"
    index_FS = url_firstchapter.rfind('/')  #从右到左定位第一个正斜杠的位置
    #url_chapters = url_firstchapter[0:32]  #截取字符串包括尾部的正斜杠
    url_chapters = url_firstchapter[0:index_FS+1]  #截取目录页面字符串，包括尾部的正斜杠
    pipeline=XbiqugePipeline()
    novelcollection=pipeline.get_collection(name) #获取小说数据集cursor对象，mongodb的数据集（collection）相当于mysql的数据表table
    #--------------------------------------------                   
    #如果next_page的值是小说目录页面url，则把包含目录页面的记录删除，以免再次抓取时，出现多个目录页面url，使得无法获得最新内容。
    if novelcollection.find({"next_page":url_chapters}).count() != 0 :
        print("包含目录页面url的记录:",novelcollection.find({"next_page":url_chapters},{"_id":0,"id":1,"url":1,"next_page":1}).next())
#        pdb.set_trace()
        novelcollection.remove({"next_page":url_chapters})
        print("已删除包含目录页面url的记录。")
    #--------------------------------------------
    novelcounts=novelcollection.find().count()
    novelurls=novelcollection.find({},{"_id":0,"id":1,"url":1})
    item = XbiqugeItem()
    item['id'] = novelcounts         #id置初值为colletion的记录总数
    item['name'] = name
    item['url_firstchapter'] = url_firstchapter
    item['name_txt'] = name_txt

    def start_requests(self):
        start_urls = [self.url_chapters]
        print("小说目录url:",start_urls)
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):    #网页提取数据，并与mongodb数据集比较，没有相同的数据才从网页抓取。
        f = open("/root/xbiquge_w/url_list.txt","w")   #打开文件，以便写入抓取页面url
        count_bingo=0   #数据集中已有记录的条数 
        dl = response.css('#list dl dd')     #提取章节链接相关信息
        for dd in dl:
            count_iterator = 0
            self.url_c = self.url_ori + dd.css('a::attr(href)').extract()[0]   #组合形成小说的各章节链接
            #print("网页提取url:", self.url_c)
            self.novelurls=self.novelcollection.find({},{"_id":0,"id":1,"url":1})   #通过重新赋值迭代器来重置迭代器指针，使for循环能够从头遍历迭代器。
            for url in self.novelurls:
                #print("mongodb提取url:", url)
                if url["url"]==self.url_c:      #如果数据集中找到与网页提取的url值相同，则跳出循环
                    count_bingo += 1
                    count_iterator += 1         
                    break
            if count_iterator != 0 :            #如果有命中结果，则继续下一个循环，不执行爬取动作
               continue
            #print("爬取url:",self.url_c)
            f.write("爬取url:"+self.url_c+"\n")
            #yield scrapy.Request(self.url_c, callback=self.parse_c,dont_filter=True)
            yield scrapy.Request(self.url_c, callback=self.parse_c)    #以生成器模式（yield）调用parse_c方法获得各章节链接、上一页链接、下一页链接和章节内容信息。
            #print(self.url_c)
        f.close()
        print("数据集已有记录数count_bingo:",count_bingo)       

    def parse_c(self, response):
        self.item['id'] += 1
        self.item['url'] = response.url
        self.item['preview_page'] = self.url_ori + response.css('div .bottem1 a::attr(href)').extract()[1]
        self.item['next_page'] = self.url_ori + response.css('div .bottem1 a::attr(href)').extract()[3]
        title = response.css('.con_top::text').extract()[4]
        contents = response.css('#content::text').extract()
        text=''
        for content in contents:
            text = text + content
        #print(text)
        self.item['content'] = title + "\n" + text.replace('\15', '\n')     #各章节标题和内容组合成content数据，\15是^M的八进制表示，需要替换为换行符。
        yield self.item     #以生成器模式（yield）输出Item对象的内容给pipelines模块。

        if self.item['url'][self.url_firstchapter.rfind('/')+1:self.url_firstchapter.rfind('.')] == self.item['next_page'][self.url_firstchapter.rfind('/')+1:self.url_firstchapter.rfind('.')]: #同一章有分页的处理
            self.url_c = self.item['next_page']
            yield scrapy.Request(self.url_c, callback=self.parse_c)
