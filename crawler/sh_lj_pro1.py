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
import random
import requests

class lj_2sf:

    #初始化
    def __init__(self):
        #起始链接
        # self.init_url = "http://sh.lianjia.com/ershoufang/d1"
        #设置报头
        # self.headers = {
        #     'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        # }


        #报头池
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        # 加入代理
        # 加入代理
        self.enable_proxy = True
        # proxy_handler = urllib2.ProxyHandler({"http": '101.231.67.202:808'})
        # 调试阶段，不设置代理
        # self.iplist = []  ##初始化一个list用来存放我们获取到的IP
        # html = requests.get("http://haoip.cc/tiqu.htm")  ##不解释咯
        # iplistn = re.findall(r'r/>(.*?)<b', html.text,
        #                      re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
        # for ip in iplistn:
        #     i = re.sub('\n', '', ip)  ##re.sub 是re模块替换的方法，这儿表示将\n替换为空
        #     self.iplist.append(i.strip())  ##添加到我们上面初始化的list里面
        #
        # self.IP = ''.join(str(random.choice(self.iplist)).strip())  ##随机挑选IP代理地址
        #
        # self.proxy_handler = urllib2.ProxyHandler({"http": self.IP})

        # 加入cookies
        self.enable_cookie = True
        # 设置cookie
        self.cookie = cookielib.LWPCookieJar()
        # cookie处理器
        self.cookie_handler = urllib2.HTTPCookieProcessor(self.cookie)

        # 设置opener
        # self.opener = urllib2.build_opener(self.proxy_handler, self.cookie_handler, urllib2.HTTPHandler)

    #建立IP代理池
    def getIP(self):
        self.iplist = []
        html = requests.get("http://haoip.cc/tiqu.htm")  ##不解释咯
        iplistn = re.findall(r'r/>(.*?)<b', html.text,
                             re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
        for ip in iplistn:
            i = re.sub('\n', '', ip)  ##re.sub 是re模块替换的方法，这儿表示将\n替换为空

            # 测试IP代理是否可以用
            i='%s'%str(i.strip())
            print i, type(i)


            openr = urllib2.build_opener(proxy_handler)

            self.iplist.append(i.strip())  ##添加到我们上面初始化的list里面


        IP = ''.join(str(random.choice(self.iplist)).strip())  ##随机挑选IP代理地址

        print type(IP)

        #测试IP代理是否可以用

        # try:
        #     html = urllib2.urlopen('http://www.baidu.com')
        #
        # return IP

    #获取页面
    def getPage(self, url):
        try:
            # 从self.user_agent_list中随机取出一个字符串（聪明的小哥儿一定发现了这是完整的User-Agent中：后面的一半段）
            UA = random.choice(self.user_agent_list)
            headers = {'User-Agent':UA}
            request = urllib2.Request(url, headers = headers)

            #设置代理池

            proxy_handler = urllib2.ProxyHandler({"http": self.IP})

            opener = urllib2.build_opener(proxy_handler, self.cookie_handler, urllib2.HTTPHandler)

            response = opener.open(request)

            content = response.read()
        except urllib2.URLEroor, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason
            else:
                print "gePage is Wrong"

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

    #获取最大页数
    def getPageNum(self,url):
        content = self.getPage(url)
        tree = lxml.html.fromstring(content)
        PageNum = tree.xpath('//div[@class="page-box house-lst-page-box"]/a[8]/text()')
        print PageNum


    #获取页面内容
    def getDatas(self,url):
        try:

            content = self.getPage(url)
            tree = lxml.html.fromstring(content)

            #把所有的li项目抽取出来
            items = tree.xpath('//div[@class="con-box"]/div[@class="list-wrap"]/ul[@id="house-lst"]/li')

            datas = []
            #单挑li的内容解析，获取房子信息:下层链接，标题，小区，户型,面积，楼层、朝向、建造时间，距离，满五,钥匙，总价，单价，查看人数
            #楼层、建造时间、装修、朝向、首付、月供、区域、地址
            for item in items:
                # print lxml.html.tostring(item,pretty_print=True)
                #子链接
                son_url= item.xpath('div[@class="info-panel"]/h2/a/@href')
                son_url = "http://sh.lianjia.com"+son_url[0] if son_url[0] else ' '
                # 标题
                title = item.xpath('div[@class="info-panel"]/h2/a/text()')
                title = title[0] if title else ' '
                # 小区
                block = item.xpath('div[@class="info-panel"]/div[@class="col-1"]/div/a/span/text()')
                block = block[0] if block else ' '
                # 户型
                type = item.xpath('div[@class="info-panel"]/div[@class="col-1"]/div/span[1]')
                type = type[0].text.strip() if type else ' '
                # 面积
                area = item.xpath('div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span[2]/text()')
                area = area[0].strip() if area else ' '
                # 距离
                distance = item.xpath('div[@class="info-panel"]//span[@class="fang-subway-ex"]/span/text()')
                distance = distance[0].strip() if distance else ' '
                # 满五
                tax = item.xpath('div[@class="info-panel"]//span[@class="taxfree-ex"]/span/text()')
                tax = tax[0] if tax else ' '
                # 钥匙
                key = item.xpath('div[@class="info-panel"]//span[@class="haskey-ex"]/span/text()')
                key = key[0] if key else ' '
                # 总价
                price = item.xpath('div[@class="info-panel"]//div[@class="price"]/span[@class="num"]/text()')
                price = price[0] if price else ' '
                # 单价
                price_pre = item.xpath('div[@class="info-panel"]//div[@class="price-pre"]/text()')
                price_pre = price_pre[0] if price_pre else ' '
                # 查看人数
                num = item.xpath('div[@class="info-panel"]//div[@class="square"]/div/span[@class="num"]/text()')
                num = num[0] if num else ' '

                #从子页面爬取10项数据：楼层、朝向、建造时间、装修、首付、月供、区域、地址、上次交易、房屋类型
                son_data = self.getSonDatas(son_url)

                # print son_url, title, block, type, area, distance, tax, key, price, price_pre, num ,son_data[0], son_data[1], son_data[2], son_data[3], son_data[4], son_data[5], son_data[6],son_data[7], son_data[8],son_data[9]
                datas.append([son_url, title, block, type, area, distance, tax, key, price, price_pre, num ,son_data[0], son_data[1], son_data[2], son_data[3], son_data[4], son_data[5], son_data[6],son_data[7], son_data[8],son_data[9]])

        except urllib2.URLEroor, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            else:
                print "geDatas is Wrong"

        return datas

    #从子链接获取楼层、建造时间、装修、朝向、首付、月供、区域、地址
    def getSonDatas(self,url):
        try:
            content = self.getPage(url)
            tree = lxml.html.fromstring(content)
            # print lxml.html.tostring(tree,pretty_print=True)

            # 获取楼层、建造时间、装修、朝向、首付、月供、区域、地址、上次交易、房屋类型

            #楼层
            floor = tree.xpath('//div[@class="esf-top"]/div[@class="cj-cun"]/div[@class="content"]/table//tr[2]/td[1]/text()')
            floor = floor[1].strip() if floor else ' '
            # print floor

            #建造时间
            build_time = tree.xpath('//div[@class="esf-top"]/div[@class="cj-cun"]/div[@class="content"]/table//tr[2]/td[2]/text()')
            build_time = build_time[1].strip() if build_time else ' '
            # print build_time

            #装修,取出有难度，难点在于内容不再标签内
            fitment = tree.xpath('//div[@class="esf-top"]/div[@class="cj-cun"]/div[@class="content"]/table//tr[3]/td[1]/text()')
            fitment = fitment[1].strip() if fitment else ' '
            # print fitment
            #朝向
            orientation = tree.xpath('//div[@class="esf-top"]/div[@class="cj-cun"]/div[@class="content"]/table//tr[3]/td[2]/text()')
            orientation = orientation[1].strip() if orientation else ' '
            # print orientation

            #首付
            pre_pay = tree.xpath('//div[@class="esf-top"]/div[@class="cj-cun"]/div[@class="content"]/table//tr[4]/td[1]/text()')
            pre_pay = pre_pay[1].strip() if pre_pay else ' '
            # print pre_pay
            #月供
            month_pay = tree.xpath('//div[@class="esf-top"]/div[@class="cj-cun"]/div[@class="content"]/table//tr[4]/td[2]/text()')
            month_pay = month_pay[1].strip() if pre_pay else ' '
            # print month_pay
            #区域
            location = tree.xpath('//div[@class="esf-top"]/div[@class="cj-cun"]/div[@class="content"]/table//tr[5]//span[@class="areaEllipsis"]/text()')
            location = location[0].strip() if location else ' '
            # print location
            #地址
            address = tree.xpath('//div[@class="esf-top"]/div[@class="cj-cun"]/div[@class="content"]/table//tr[6]/td/p/text()')
            address = address[0].strip() if address else ' '
            # print address
            #上次交易
            last_deal = tree.xpath('//div[@class="content-wrapper introduction-wrapper js_content"]//div[@class="transaction"]//li[1]/text()')
            last_deal = last_deal[0].strip() if last_deal else ' '
            # print last_deal
            #房屋类型
            house_property = tree.xpath('//div[@class="content-wrapper introduction-wrapper js_content"]//div[@class="transaction"]//li[2]/text()')
            house_property = house_property[0].strip() if house_property else ' '
            # print house_property

            #返回这7个属性的内容
            data = [floor,build_time,fitment,orientation,pre_pay,month_pay,location,address,last_deal,house_property]


        except urllib2.URLEroor, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            else:
                print "geSonData is Wrong"

        # print datas
        return data


    #存储模块
    #CSV文件初始化
    def init_Csv(self):
        csvfile = open('sh_lj_2s_pro.csv', 'wb')
        writer = csv.writer(csvfile)
        writer.writerow(['具体链接','标题','小区','户型','面积','距离','满五','钥匙','总价','单价','查看人数',\
                         '楼层','建造时间','装修','朝向','首付','月供','区域','地址','上次交易','房屋类型'])
        csvfile.close()

    #保存到CSV
    def SaveCsv(self,url):

        #写入数据
        csvfile = open('sh_lj_2s_pro.csv', 'ab')
        writer = csv.writer(csvfile)


        datas = self.getDatas(url)

        for data in datas:
            csv_data = []
            for item in data:
                item = item.strip().encode('utf-8')
                csv_data.append(item)
            writer.writerow(csv_data)

        csvfile.close()
        # print "csv_sh_lj_2s.csv has been saved."

        # csv的读取
        # csvfile_read = open('csv_sh_lj_2s.csv', 'rb')
        # reader = csv.reader(csvfile_read)
        #
        # for line in reader:
        #     print line
        #
        # csvfile_read.close()


    #启动器
    def start(self,url,csv_control=False):

        # self.IP = self.getIP()
        self.IP = '111.177.124.140:9999'
        print self.IP

         #是否初始化CSV
        if csv_control:
            self.init_Csv()

        #开始写入:
        i=12
        while i<101:
            # url = "http://sh.lianjia.com/ershoufang/d"+str(i)
            url = url[0:-1]+str(i)
            print url
            # datas = self.getDatas(url)
            self.SaveCsv(url)
            print "Page %s finished" % (str(i))
            i +=1

        print "The porject of lianjia_ershoufang is finished"













url = "http://sh.lianjia.com/ershoufang/d1"
url1 = "http://sh.lianjia.com/ershoufang/sh4499373.html"
test = lj_2sf()
# test.getDatas(url)
# test.init_Csv()
# test.getPageNum(url)
# test.start(url)
test.getIP()








