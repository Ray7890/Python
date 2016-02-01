#!/usr/bin/env python
# encoding: utf-8
import time
import requests
from bs4 import BeautifulSoup
import random
# 把str编码由ascii改为utf8（或gb18030）
import sys
reload(sys)
sys.setdefaultencoding('utf8')


file_name = 'bbs_list.txt'
file_content = ''  # 最终要写到文件里的内容
file_content += '生成时间：' + time.asctime()

headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
]


def bbs_spider():
    global file_content, headers
    # 贴吧Python
    url = "http://tieba.baidu.com/f?ie=utf-8&kw=python" 
    source_code = requests.get(url, headers=random.choice(headers))
    # just get the code, no headers or anything
    plain_text = source_code.text
    # BeautifulSoup objects can be sorted through easy
    soup = BeautifulSoup(plain_text)

    
    count = 1    
    # 得到BBS列表的soup对象
    list_soup = soup.find('div', {'class': 'content_leftList clearfix'})
    for bbs_info in list_soup.findAll('a', class_="j_th_tit"):
        print '_' * 80
        title = bbs_info.string.strip()

        print "Title %d: %s " %  (count, title)   
        file_content += "Title %d:《%s》\n" % (count, title) 
        count = count + 1

bbs_spider()
# 将最终结果写入文件
f = open(file_name, 'w')
f.write(file_content)
f.close()
