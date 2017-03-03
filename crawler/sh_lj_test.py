#!/usr/bin/python
# encoding: utf-8

"""
@author: ocean
@contact: dazekey@163.com
@file:sh_lj_test.py
@time:2017/3/2 10:29
"""


import urllib
import urllib2
import re
import cookielib
from bs4 import BeautifulSoup
import tool
import lxml.html
from lxml import etree


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

# soup = BeautifulSoup(content,'lxml')
# print soup.prettify()

#对象为soup

#搜索行政区域
# items = soup.find('div',class_="option-list gio_district").find_all('a',class_="")
# # print items
# for item in items:
#     district = item.get_text()
#     print district

#获取房子信息:下层链接，标题，小区，户型,面积，楼层、朝向、建造时间，距离，满五,钥匙，总价，单价，查看人数
# items2 = soup.find('ul',id="house-lst").find_all('li')
# # print items2
# for item in items2:
#     #子链接
#     url = item.find('h2').a.get('href')
#     #标题
#     title = item.find('h2').a.get_text()
#     #小区
#     block = item.find('div',class_='col-1').a.get_text()
#     #户型
#     type = item.find('div',class_='where').find_all('span')[1].get_text()
#     #面积
#     area = item.find('div',class_='where').find_all('span')[2].get_text()
#
#     #楼层、朝向、建造时间比较难获取
#     text = item.find('div',class_='con').get_text()
#     text = text.replace("\n","").replace("\t","").replace(" ","").split("|")
#
#     #楼层
#     floor =text[1]
#     #朝向
#     orientation = text[2]
#     #建造时间
#     if len(text) ==4:
#         buildtime = text[3]
#     else:
#         buildtime = " "
#
#     #距离
#     distance = item.find('span',class_="fang-subway-ex").span.get_text()
#
#     #满五免税
#     tax = item.find('span',class_="taxfree-ex").span.get_text()
#
#     #钥匙
#     key = item.find('span',class_='haskey-ex').span.get_text()
#
#     #总价
#     price = item.find('span',class_="num").get_text()
#
#     #单价
#     price_pre = item.find('div',class_="price-pre").get_text()
#
#     #查看人数
#     num_look = item.find('div',class_='square').span.get_text()
#
#     print url,title,block,area,floor,orientation,distance,tax,key,price,price_pre,num_look



#使用xpath分析网页信息

#用lml.html.fromstring和tostring模块处理网页
tree = lxml.html.fromstring(content)
# print type(tree)
html = lxml.html.tostring(tree,pretty_print=True)
# content = content.encode('utf-8')
# html = etree.HTML(content)
# html = etree.tostring(html)
# print html

#获取行政区列表
# results = tree.xpath('//div[@class="option-list gio_district"]/div[@class="item-list"]/a')
# for district in results:
#     print district.text
#
# district_url = tree.xpath('//div[@class="option-list gio_district"]/div[@class="item-list"]/a/@href')
# for district_url in district_url:
#     print 'http://sh.lianjia.com/ershoufang'+district_url

#获取房子信息:下层链接，标题，小区，户型,面积，楼层、朝向、建造时间，距离，满五,钥匙，总价，单价，查看人数

#下层链接
urls = tree.xpath('//li/div[@class="info-panel"]/h2/a/@href')
# for url in urls:
#     print 'http://sh.lianjia.com'+url

#标题
titles = tree.xpath('//li/div[@class="info-panel"]/h2/a')
# for title in titles:
#     print title.text

#小区
blocks = tree.xpath('//li/div[@class="info-panel"]/div[@class="col-1"]/div/a/span')
# for block in blocks:
#     print block.text

#户型
types = tree.xpath('//li/div[@class="info-panel"]/div[@class="col-1"]/div/span[1]')
# for type in types:
#     print type.text

#面积
areas = tree.xpath('//li/div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span[2]')
# for area in areas:
#     print area.text

#难点，楼层、朝向、建造年代的内容居然再标签外

texts = tree.xpath('//li/div[@class="info-panel"]/div[@class="col-1"]/div[@class="other"]/div[@class="con"]')
# print texts
#楼层
floors = []
#朝向
orientations = []
#建造时间
buildtimes = []
for text in texts:
    text = text.xpath('string(.)')
    text = text.replace("\n","").replace(" ","").replace("\t","").split("|")
    floors.append(text[1])
    orientations.append(text[2])
    if len(text)==4:
        buildtimes.append(text[3])
    else:
        buildtimes.append(" ")

# for floor in floors:
#     print floor
#
# for orientation in orientations:
#     print orientation
#
# for buildtime in buildtimes:
#     print buildtime

#距离
distances = tree.xpath('//span[@class="fang-subway-ex"]/span')
# for distance in distances:
#     print distance.text

#满五
taxes = tree.xpath('//span[@class="taxfree-ex"]/span')
# for tax in taxes:
#     print tax.text

#钥匙
keys = tree.xpath('//span[@class="haskey-ex"]/span')
# for key in keys:
#     print key.text

#总价
prices = tree.xpath('//span[@class="num"]')
# for price in prices:
#     print price.text

#单价
prices_pre = tree.xpath('//div[@class="price-pre"]')
# for price_pre in prices_pre:
#     print price_pre.text

#查看人数
nums = tree.xpath('//div[@class="square"]/div/span[@class="num"]')
# for num in nums:
#     print num.text


#获取房子信息:下层链接，标题，小区，户型,面积，楼层、朝向、建造时间，距离，满五,钥匙，总价，单价，查看人数
datas = []
i = 0
while i <len(urls):
    url = "http://sh.lianjia.com"+urls[i]
    title = titles[i].text
    block = blocks[i].text
    type = types[i].text
    area = areas[i].text
    floor = floors[i]
    orientation = orientations[i]
    buildtime = buildtimes[i]
    distance = distances[i].text
    tax = taxes[i].text
    key = keys[i].text
    price = prices[i].text
    price_pre =prices_pre[i].text
    num = nums[i].text

    datas.append([url,title,block,type,area,floor,orientation,buildtime,distance,tax,key,price,price_pre,num])
    i += 1

for data in datas:
    print data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13]

#数据存储
#存储到TXT

#存储到CSV



#存储到MySQL













