# -*- coding: utf-8 -*-
import scrapy
from xbiquge.items import XbiqugeItem
from xbiquge.pipelines import XbiqugePipeline

class SancunSpider(scrapy.Spider):
    name = 'sancun'
    allowed_domains = ['www.xbiquge.la']
    #start_urls = ['http://www.xbiquge.la/10/10489/']
    url_ori= "https://www.xbiquge.la"
    url_firstchapter = "https://www.xbiquge.la/10/10489/4534454.html"
    name_txt = "./novels/三寸人间"
    url_chapters = url_firstchapter[0:32]
    pipeline=XbiqugePipeline()
    #pipeline.clearcollection(name) #清空小说的数据集合（collection），mongodb的collection相当于mysql的数据表table
    novelcollection=pipeline.get_collection(name)
    #如果next_page的值是小说目录页面url，则把包含目录页面的记录删除，以免再次抓取时，出现多>个目录页面url，使得无法获得最新内容。
    if novelcollection.find({"next_page":url_chapters}).count() != 0 :
        print("包含目录页面url的记录数:",novelcollection.find({"next_page":url_chapters}).count())
        novelcollection.remove({"next_page":url_chapters})
    novelcounts=novelcollection.find().count()
    novelurls=novelcollection.find({},{"_id":0,"id":1,"url":1})
    item = XbiqugeItem()
    #item['id'] = 0         #新增id字段，便于查询
    item['id'] = novelcounts         #id置初值为colletion的记录总数
    item['name'] = name
    item['url_firstchapter'] = url_firstchapter
    item['name_txt'] = name_txt

    def start_requests(self):
        start_urls = [self.url_chapters]
        #print(start_urls)
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        count_bingo=0   
        dl = response.css('#list dl dd')     #提取章节链接相关信息
        for dd in dl:
            self.url_c = self.url_ori + dd.css('a::attr(href)').extract()[0]   #组合形成小说的各章节链接
            #print("网页提取url:", self.url_c)
            count_iterator=0
            self.novelurls=self.novelcollection.find({},{"_id":0,"id":1,"url":1})   #重置迭代器指针，使for循环能够遍历迭代器
            for url in self.novelurls:
                #print("mongodb提取url:", url)
                if url["url"]==self.url_c:      #如果数据库中找到与网页提取的url值相同，则跳出循环
                    count_iterator += 1
                    count_bingo += 1
                    #print("count_iterator:",count_iterator)
                    break
            if count_iterator != 0 :            #如果有命中结果，则继续下一个循环，不执行爬取动作
               continue
            print("爬取url:",self.url_c)
            #yield scrapy.Request(self.url_c, callback=self.parse_c,dont_filter=True)
            yield scrapy.Request(self.url_c, callback=self.parse_c)    #以生成器模式（yield）调用parse_c方法获得各章节链接、上一页链接、下一页链接和章节内容信息。
            #print(self.url_c)
        print("数据库已有记录数count_bingo:",count_bingo)       

    def parse_c(self, response):
        #item = XbiqugeItem()
        #item['name'] = self.name
        #item['url_firstchapter'] = self.url_firstchapter
        #item['name_txt'] = self.name_txt
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

        if self.item['url'][31:38] == self.item['next_page'][31:38]: #同一章有分页的处理
            self.url_c = self.item['next_page']
            yield scrapy.Request(self.url_c, callback=self.parse_c)
