# -*- coding:utf-8 -*-
import requests
from lxml import etree
import time
import sys

def getfrombing(word):
    url = 'http://global.bing.com/search?q='+word+'&qs=bs&ajf=60&first=1&Accept-Language=en-us'
    list = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }

    flag0 = 3
    #爬取网页的数量
    for k in range(0,11):
        path = etree.HTML(requests.get(url=url, headers=headers).content.decode('utf-8'))
        flag=15
        if k == 0:
            flag=9
        for i in range(1,flag):
            words=""
            for j in path.xpath('//*[@id="b_results"]/li[%d]/h2/a//text()'%i):
                words+=j
            if len(words)>0:
                print(words)
                list.append(words)
                pass
            pass
        flag0+=flag-1
        url='http://global.bing.com/search?q='+word+'&qs=bs&ajf=60&first='+str(flag0)+'&Accept-Language=en-us'
        print(url)
        time.sleep(10)
    return list

if __name__ == '__main__':
    getfrombing('云从科技')
