#!/usr/bin/env python
# encoding: utf-8
import time
import requests
from bs4 import BeautifulSoup
import random
import MySQLdb

# 把str编码由ascii改为utf8（或gb18030）
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Define the Brower Header

class bbs_spider:
        def __init__(self):
                self.headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
                ]
                # 连接数据库
                self.conn = MySQLdb.connect(host='127.0.0.1', user='python', passwd='python7890', charset='utf8')
                self.cur = self.conn.cursor()
                self.conn.select_db('python_db')
                # Base URL
                self.base_url = "http://tieba.baidu.com/f?kw=python&ie=utf-8&pn="    

        def get_titleinfo(self, max_item_num = 1000):
                #
                item_num = 0
                step = 50

                while (item_num < max_item_num):
                        # new url
                        url = self.base_url + "%d" % (item_num)
                        print "URL: ", url

                        source_code = requests.get(url, headers=random.choice(self.headers))
                        plain_text = source_code.text
                        # BeautifulSoup objects can be sorted through easy
                        soup = BeautifulSoup(plain_text)

                        # 得到BBS列表的soup对象
                        list_soup = soup.find('div', {'id': 'content_leftList'})
                        # Get every topic info
                        for bbs_info in list_soup.findAll('li', class_="j_thread_list clearfix"):
                                try:
                                        title = bbs_info.find('a', class_="j_th_tit").string.strip()
                                        reply_num = bbs_info.find('div', {'class': 'threadlist_rep_num'}).string.strip()
                                        rep_num = int(reply_num)
                                except AttributeError:
                                        title = "Exception"

                                sql = "insert into python_bbs_title (title, reply_num)\
                                        values ('%s', %d);" % (title, rep_num)
                                try:
                                        self.cur.execute(sql)
                                except Exception as e:
                                        print type(e), e
                                        pass
                        item_num = item_num + step

                # 关闭数据库连接
                self.cur.close()
                self.conn.commit()
                self.conn.close()

# 
get_bbs = bbs_spider()
get_bbs.get_titleinfo(200)
