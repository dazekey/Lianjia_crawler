#!/usr/bin/python
# encoding: utf-8

"""
@author: ocean
@contact: dazekey@163.com
@file:sh_lj_test.py
@time:2017/3/2 10:29
"""


import urllib #网页解析库
import urllib2 #网页解析库
import re  # 正则表达式的库
import cookielib  #cookie的库
from bs4 import BeautifulSoup  # BeautifulSoup的库
import lxml.html  # lxml xpath的库
from lxml import etree # lxml xpath的库
import csv #csv的库
from mysql import connector  # 连接MySQL的库

tool = tool.Tool()

url = 'http://sh.lianjia.com/ershoufang/d1'
# url = 'http://land.fang.com/market/510100________1_0_1.html'


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
# #只匹配行政区
# pattern_district = re.compile('<a href="/ershoufang.*?class="" >(.*?)</a>', re.S)

# #错误方法
# pattern_district = re.compile('<a href="(.*?)" gahref=".*? class="" >(.*?)</a>', re.S)
# districts = re.findall(pattern_district, content)
# for district in districts:
#     print district
#
# #打包拿下行政区和链接
# pattern_district = re.compile('<a href="/ershoufang/".*?</a>.*?<div class="item-list">(.*?)</div>',re.S)
#
# districts = re.findall(pattern_district, content)
# districts =districts[0]
# print districts
#
# #把链接和行政区分别取出
# pattern = re.compile('<a href="(.*?)" gahref.*?>(.*?)</a>',re.S)
# item = re.findall(pattern,districts)
#
# print item
#
# for i in item:
#     print i[0], i[1]



#
#
# 对象是content，用正则表达式去匹配房子信息:下层链接，小区，户型,面积，楼层、朝向、建造时间，描述1,描述2，描述3，总价，单价，查看人数
# 无法匹配到<span>| </span>下 楼层、朝向、建造时间的内容
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
# print type(content)
# soup = BeautifulSoup(content,'lxml')
# print type(soup.prettify())
#
# #对象为soup
#
# # 搜索行政区域
# items = soup.find('div',class_="option-list gio_district").find_all('a',class_="")
# # print items
# for item in items:
#     district = item.get_text()
#     district_url = item.get('href')
#     print district,district_url
#
# # 获取房子信息:下层链接，标题，小区，户型,面积，楼层、朝向、建造时间，距离，满五,钥匙，总价，单价，查看人数
# items2 = soup.find('ul',id="house-lst").find_all('li')
# # print items2
# datas = []
# for item in items2:
#     #子链接
#     url = item.find('h2').a.get('href')
#     url = "http://sh.lianjia.com"+url
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
#     if item.find('span',class_="fang-subway-ex"):
#         distance = item.find('span',class_="fang-subway-ex").span.get_text()
#     else:
#         distance = " "
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
#     print url,title,block,type,area,floor,orientation,buildtime,distance,tax,key,price,price_pre,num_look
#     datas.append([url,title,block,type,area,floor,orientation,buildtime,distance,tax,key,price,price_pre,num_look])
#     #子链接，标题，小区，户型,面积，楼层、朝向、建造时间，距离，满五,钥匙，总价，单价，查看人数



#使用xpath分析网页信息

#用lml.html.fromstring和tostring模块处理网页
tree = lxml.html.fromstring(content)
# print type(tree)
html = lxml.html.tostring(tree,pretty_print=True)
# content = content.encode('utf-8')
# tree = etree.HTML(content)
# html = etree.tostring(html)
# print html

# # 获取行政区列表
# results = tree.xpath('//div[@class="option-list gio_district"]/div[@class="item-list"]/a')
# for district in results:
#     print district.text
#
# # 获取行政区链接
# district_url = tree.xpath('//div[@class="option-list gio_district"]/div[@class="item-list"]/a/@href')
# for district_url in district_url:
#     print 'http://sh.lianjia.com/ershoufang'+district_url

#获取房子信息:下层链接，标题，小区，户型,面积，楼层、朝向、建造时间，距离，满五,钥匙，总价，单价，查看人数

#下层链接
urls = tree.xpath('//li/div[@class="info-panel"]/h2/a/@href')
# print len(urls)
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

#难点处理，楼层、朝向、建造年代的内容居然再标签外

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
#建立文件
#设置文件名
# title = "sh_lianjia_ershoufang"
# #打开要写的文件，没有的话创建，参数w表示重新写入
# file = open(title+".txt","w")
#
# #开始写入文件
# for data in datas:
#     # data = data.encode('utf-8')
#     file_data = []
#     for item in data:
#         item = item.strip().encode('utf-8')
#         #不能写入列表，只能一个一个写入,默认空格区分
#         file.write(item+",")
#     file.write("\n")
#     # print file_data
#     # file.write(file_data)
#
# print title+" is writed"
#
# #txt的内容读取
# file = open("sh_lianjia_ershoufang.txt","r")
# f = file.readlines()
# print f
# for i in f:
#     print i
#
# file.close()


#存储到CSV
# csvfile = open('csv_sh_lj_2s.csv','wb')
# writer = csv.writer(csvfile)
#
# for data in datas:
#     csv_data = []
#     for item in data:
#         item = item.strip().encode('utf-8')
#         csv_data.append(item)
#     writer.writerow(csv_data)
#
#
# csvfile.close()
# print "csv_sh_lj_2s.csv has been saved."
#
# #csv的读取
# csvfile_read = open('csv_sh_lj_2s.csv','rb')
# reader = csv.reader(csvfile_read)
#
# for line in reader:
#     print line
#
# csvfile_read.close()



#存储到MySQL
#创建链接
params = dict(host='localhost',port = 3306 ,user ='root',password = '', database='test')
conn = connector.connect(**params)

#创建指标
cursor= conn.cursor()

#创建表:下层链接，标题，小区，户型,面积，楼层、朝向、建造时间，距离，满五,钥匙，总价，单价，查看人数
ddl = """
    create table lianjia_sh(id integer, url varchar(100), title varchar(100), block varchar(100), type varchar(100), area varchar(100), floor varchar(100), orientation varchar(100), buildtime varchar(100), distance varchar(100), tax varchar(100), have_key varchar(100), price varchar(100), price_pre varchar(100), num varchar(100))
"""

#插入内容：
sqltext = """
    insert into lianjia_sh(url,title,block,type,area,floor,orientation,buildtime,distance,tax,have_key,price,price_pre,num) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""
# for data in datas:
#     cursor.execute(sqltext,data)
#     conn.commit()

# data_eg = ['/ershoufang/sh4281292.html','温馨之家，业主诚意出售，链家推荐，好房待售','梅陇二村','45.01平 ','中区/6层','朝南','1988年建','距离1号线莲花路站832米','满五','有钥匙','240','53321元/平','85']

cursor.executemany(sqltext,datas)

#指针提交，不然回滚
conn.commit()

conn.close



















