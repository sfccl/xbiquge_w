import os
while(True):
    os.system('scrapy crawl sancun -s CLOSESPIDER_TIMEOUT=120')
    os.system('scrapy crawl djzs -s CLOSESPIDER_TIMEOUT=120')
