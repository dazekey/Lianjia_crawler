#!/usr/bin/python
# _*_ coding:utf-8 _*_

import urllib
import urllib2
import re
import cookielib
import gzip
import StringIO
import lxml.html
from lxml import etree
import csv
import time
import pandas

class lj_2sf:

    #初始化
    def __init__(self):
        #起始链接
        self.init_url = "http://sh.lianjia.com/ershoufang/d1"
        #设置报头
        self.headers = headers = {
            'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

        #加入代理
        # 加入代理
        self.enable_proxy = True
        # proxy_handler = urllib2.ProxyHandler({"http": '101.231.67.202:808'})
        # 调试阶段，不设置代理
        self.proxy_handler = urllib2.ProxyHandler({})

        # 加入cookies
        self.enable_cookie = True
        # 设置cookie
        self.cookie = cookielib.LWPCookieJar()
        # cookie处理器
        self.cookie_handler = urllib2.HTTPCookieProcessor(self.cookie)

        # 设置opener
        self.opener = urllib2.build_opener(self.proxy_handler, self.cookie_handler, urllib2.HTTPHandler)


    #获取页面
    def getPage(self, url):
        request = urllib2.Request(url, headers = self.headers)
        response = self.opener.open(request)
        content = response.read()

        #链家居然不要解压也不需要解码，良心
        # print content
        return content

    #获取行政区信息
    def getDistrict(self,url):
        content = self.getPage(url)
        tree = lxml.html.fromstring(content)

        # 获取行政区列表
        districts = tree.xpath('//div[@class="option-list gio_district"]/div[@class="item-list"]/a')
        datas = []
        # for district in districts:
            # print district.text

        # 获取行政区链接
        district_urls = tree.xpath('//div[@class="option-list gio_district"]/div[@class="item-list"]/a/@href')
        # for district_url in district_urls:
        #     district_url = "http://sh.lianjia.com"+district_url
            # print district_url

        i=0
        while i < len(districts):
            # print districts[i].text
            datas.append([districts[i].text,"http://sh.lianjia.com"+district_urls[i]])
            i += 1

        # for data in datas:
        #     print data[0],data[1]

        return datas

    #获取页面内容
    def getDatas(self,url):
        content = self.getPage(url)
        tree = lxml.html.fromstring(content)

        #把所有的li项目抽取出来
        items = tree.xpath('//div[@class="con-box"]/div[@class="list-wrap"]/ul[@id="house-lst"]/li')

        #单挑li的内容解析，获取房子信息:下层链接，标题，小区，户型,面积，楼层、朝向、建造时间，距离，满五,钥匙，总价，单价，查看人数
        for item in items:
            #子链接
            son_url= item.xpath('div[@class="info-panel"]/h2/a/@href')
            son_url = "http://sh.lianjia.com"+son_url[0] if son_url[0] else ' '
            # 标题
            title = item.xpath('div[@class="info-panel"]/h2/a/text()')
            title = title[0] if title else ' '
            # 小区
            block = item.xpath('div[@class="info-panel"]/div[@class="col-1"]/div/a/span/text()')
            block = block[0] if block else ' '
            

            #从子页面爬取楼层、建造时间、装修、朝向、首付、月供、区域、地址、上次交易、房屋类型
            # son_data = getSonDatas(son_url)

            print block




        # 户型
        types = tree.xpath('//li/div[@class="info-panel"]/div[@class="col-1"]/div/span[1]')
        # 面积
        areas = tree.xpath('//li/div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span[2]')

        #楼层、建造时间、装修、朝向、首付、月供、区域、地址、上次交易、房屋类型 都可以从子页面爬取
        # son_datas = []
        # for son_url in son_urls:
        #     son_data = getSonDatas("http://sh.lianjia.com"+son_url)
        #     son_datas.append(son_data)


        # 距离
        distances = tree.xpath('//span[@class="fang-subway-ex"]/span')
        # 满五
        taxes = tree.xpath('//span[@class="taxfree-ex"]/span')
        # 钥匙
        keys = tree.xpath('//span[@class="haskey-ex"]/span')
        # 总价
        prices = tree.xpath('//span[@class="num"]')
        # 单价
        prices_pre = tree.xpath('//div[@class="price-pre"]')
        # 查看人数
        nums = tree.xpath('//div[@class="square"]/div/span[@class="num"]')

    #从子链接获取楼层、建造时间、装修、朝向、首付、月供、区域、地址、上次交易、房屋类
    def getSonDatas(self,url):
        content = self.getPage(url)
        tree = lxml.html.fromstring(content)











url = "http://sh.lianjia.com/ershoufang/d1"
test = lj_2sf()
test.getDatas(url)












