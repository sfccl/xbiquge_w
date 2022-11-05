# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import random
from .proxies import proxy_list
import os

class XbiqugeSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class XbiqugeDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        location = os.getcwd() + '/xbiquge/fake_useragent.json'  #2022-11-05修改，以解决“FakeUserAgentError('Maximum amount of retries reached')”
        #print(location)
        self.ua = UserAgent(path=location)                       #此处原为self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault("User-Agent", get_ua())

class XbiqugeCookieMiddleware(object):
    def process_request(self, request, spider):
        cookies = self.get_cookies()
        request.cookies = cookies

    def get_cookies(self):
        cookie = 'Hm_lvt_56844e6b74c4d3517aa12fcc1561e5c3=1659977978; bcolor=; font=; size=; fontcolor=; width=; PHPSESSID=7vh8vodsr9u7flj8fb0c34vk13; Hm_lvt_c88891805dd27a5878c8ee6312582d4b=1659977998; Hm_lpvt_c88891805dd27a5878c8ee6312582d4b=1659982563; Hm_lpvt_56844e6b74c4d3517aa12fcc1561e5c3=1660005610'
        cookies = {}
        c_list = cookie.split(';')
        for c in c_list:
            cookies[c.split('=')[0]] = c.split('=')[1]
        return cookies

class XbiqugeProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(proxy_list)
        request.meta['proxy'] = proxy

    #使用process_exception()处理异常
    #有些proxy不能用时，需要处理异常：方法时再让他选代理
    def process_exception(self, request, exception, spider):
        #将request请求对象再次交给中间件，继续找proxy，一直找到能用的proxy
        return request
