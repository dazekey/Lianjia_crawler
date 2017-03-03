#!/usr/bin/python
# encoding: utf-8

"""
@author: ocean
@contact: dazekey@163.com
@file:sh_lianjia.py
@time:2017/2/26 14:41
"""

import urllib
import urllib2
import re
import cookielib
from bs4 import BeautifulSoup
import tool

tool = tool.Tool()

url = 'http://sh.lianjia.com/ershoufang/d1'

#加入报头
headers = {
    'Referer':'http://sh.lianjia.com/ershoufang/d1',
    'User - Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

#加入代理
enable_proxy = True
# proxy_handler = urllib2.ProxyHandler({"http": '101.231.67.202:808'})
#调试阶段，不设置代理
proxy_handler = urllib2.ProxyHandler({})
# null_proxy_handler = urllib2.ProxyHandler({})
# if enable_proxy:
#     opener = urllib2.build_opener(proxy_handler,urllib2.HTTPHandler)
# else:
#     opener = urllib2.build_opener(null_proxy_handler,urllib2.HTTPHandler)
# urllib2.install_opener(opener)

#加入cookies
enable_cookie = True
#设置cookie
cookie = cookielib.LWPCookieJar()
#cookie处理器
cookie_handler = urllib2.HTTPCookieProcessor(cookie)
# null_cookie_handler = urllib2.HTTPCookieProcessor({})
# if enable_cookie:
#     opener = urllib2.build_opener(cookie_handler,urllib2.HTTPHandler)
# else:
#     opener = urllib2.build_opener(null_cookie_handler,urllib2.HTTPHandler)

#同时加入proxy和cookie
opener = urllib2.build_opener(proxy_handler,cookie_handler,urllib2.HTTPHandler)

request = urllib2.Request(url, headers=headers)
# response = urllib2.urlopen(request)
response = opener.open(request)
content = response.read()

# print content


# #用正则表达式找到行政区域
# pattern_district = re.compile('<a href="/ershoufang/.*?class="" >(.*?)</a>', re.S)
# districts = re.findall(pattern_district, content)
# for district in districts:
#     print district
#
#
#
# # 对象是content，用正则表达式去匹配房子信息:下层链接，小区，户型,面积，楼层、朝向、建造时间，描述1,描述2，描述3，总价，单价，查看人数
# # 无法匹配到<span>| </span>下 楼层、朝向、建造时间的内容
# pattern = re.compile('<div class="info-panel">.*?<h2>.*?<a name.*? href="(.*?)" title'
#                      '.*?<div class="col-1">.*?<span class="nameEllipsis".*?>(.*?)</span>'
#                      '</a>&nbsp;&nbsp;.*?<span>(.*?)&nbsp;&nbsp;</span>'
#                      '.*?<span>(.*?)&nbsp;&nbsp;</span>'
#                      # '.*?<div class="other">.*?<a href=.*?<span>| </span>(.*?)</div>.*?<div class="chanquan">'
#                      '.*?<div class="other">.*?<a href=.*?</span>(.*?)</div>.*?<div class="chanquan">'
#                      # '.*?<div class="other">.*?<a href=.*?<span>|(*?)</div><div class="chanquan">'
#                      '.*?<span class="fang-subway-ex"><span>(.*?)</span></span>'
#                      '.*?<span class="taxfree-ex"><span>(.*?)</span></span>'
#                      '.*?<span class="haskey-ex"><span>(.*?)</span></span>'
#                      '.*?<span class="num">(.*?)</span>'
#                      '.*?<div class="price-pre">(.*?)</div>'
#                      '.*?<span class="num">(.*?)</span>'
#                      , re.S)
# items = re.findall(pattern, content)
# # print items
# new_item = []
# for item in items:
#     # print item[5],item[6],item[7],item[8],item[9],item[10]
#     # print item[0],item[1],item[2],item[3],item[4]
#
#     #g给子项链接补完
#     new_item0 = "http://sh.lianjia.com" + item[0]
#
#     #难点，楼层、朝向和建造时间需要再处理提取
#     new_item4 = item[4].strip()
#     new_item4 = new_item4.replace('\n','')
#     # new_item4 = new_item4.replace(' ','')
#     new_item4 = new_item4.replace('\t', '')
#     new_item4 = new_item4.split('<span>| </span>')
#
#     #建造时间不是每一项都有，对于没有的要补完
#     if len(new_item4)<3:
#         new_item4.append(' ')
#     # print new_item4
#
#     #创建新的字段
#     new_item.append([new_item0,item[1],item[2],item[3],new_item4[0],new_item4[1],new_item4[2],item[5],item[6],item[7],item[8],item[9],item[10]])
#
# for i in new_item:
#     print i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12]



#使用soup对网页处理



soup = BeautifulSoup(content,'lxml')
print soup.prettify()

#对象为soup

#搜索行政区域
districts = soup.find_all('a', class_="",)
for district in districts:
    print district

# pattern = re.compile('<div class="info-panel">.*?<h2><a gahref.*? href="(.*?)" key',re.S)
# items = soup.find_all('li')
# print items
# for item in items:
#     print item.string
# for item in items:
#     print item
