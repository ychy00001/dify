#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Charles on 2018/10/10
# Function:

import sys
import requests
from bs4 import BeautifulSoup
import random
import time
from lxml import html, etree
import logging
import json

ABSTRACT_MAX_LENGTH = 300    # abstract max length

def get_proxy():
    return requests.get("http://10.128.172.93:13011/get/").json()

# 解析Cookie
# 请求头信息
HEADERS = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Encoding': 'gzip, deflate, compress',
      'Accept-Language': 'en-us;q=0.5,en;q=0.3',
      'Cache-Control': 'max-age=0',
      'Connection': 'keep-alive',
      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}

def calculate_num_pages(num_results, results_per_page):
    return (num_results + results_per_page - 1) // results_per_page

def bing_search(query, num_results=10, results_per_page=10):
    base_url = 'http://global.bing.com/search?q='+query+'&qs=bs&ajf=60&first=1&Accept-Language=en-us'
    num_pages = calculate_num_pages(num_results, results_per_page)
    search_results = []
    logging.info("Bing Engine Search : num_results: %s, results_per_page: %s, num_pages: %s", num_results, results_per_page ,num_pages )
#     print("Bing Engine Search : num_results: %s, results_per_page: %s, num_pages: %s", num_results, results_per_page ,num_pages )
    for page in range(1, num_pages + 1):
#         params = {
#            "q": query,
#            "first": (page - 1) * results_per_page + 1,
#            "qs":"bs",
#            "ajf":60,
#            "Accept-Language":"en-us"
#         }
#         params["random_param"] = random.randint(1, 1000)
        headers = HEADERS
        proxy = get_proxy().get("proxy")
        logging.info("Bing Engine Search use proxy: %s", proxy )
#         print("Bing Engine Search use proxy: %s", proxy )
        response = requests.get(url=base_url, headers=headers, proxies={"http": "http://{}".format(proxy)})
        logging.info("Bing Engine Search url: %s", base_url )
#         print("Bing Engine Search url: %s", base_url )
        if response.status_code == 200:
            tree = html.fromstring(response.text)
            results = tree.xpath('//li[@class="b_algo"]')
            logging.info("Bing Engine Search a_algo element: %s", results )
#             print("Bing Engine Search a_algo element: %s", results )
            for result in results[:num_results]:
                title = result.xpath('.//h2/a')[0].text_content() if len(result.xpath('.//h2/a')) > 0 else  ""
                description = result.xpath('.//p')[0].text_content() if len(result.xpath('.//p')) > 0 else ""
                url = result.xpath('.//h2/a/@href')[0] if len(result.xpath('.//h2/a/@href')) > 0 else ""

                result_dict = {"title": title, "description": description, "url": url}
                search_results.append(result_dict)

        else:
            logging.info("Bing Search Error: %s", response.status_code)
    logging.info("Bing Engine Search Result: %s", json.dumps(search_results,ensure_ascii=False))
    return search_results



def run():
    """
    主程序入口，支持命令得带参执行或者手动输入关键字
    :return:
    """
    default_keyword = u"长风破浪小武哥"
    num_results = 3
    debug = 0

    prompt = """
    baidusearch: not enough arguments
    [0]keyword: keyword what you want to search
    [1]num_results: number of results
    [2]debug: debug switch, 0-close, 1-open, default-0
    eg: baidusearch NBA
        baidusearch NBA 6
        baidusearch NBA 8 1
    """
    if len(sys.argv) > 3:
        keyword = sys.argv[1]
        try:
            num_results = int(sys.argv[2])
            debug = int(sys.argv[3])
        except:
            pass
    elif len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        print(prompt)
        keyword = input("please input keyword: ")
        # sys.exit(1)
    if not keyword:
        keyword = default_keyword
    results = bing_search(keyword, num_results=num_results)
    print(json.dumps(results,ensure_ascii=False))

if __name__ == '__main__':
    run()