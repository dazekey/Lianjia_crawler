#!/usr/bin/python
# _*_ coding:utf-8 _*_

#加入日志功能
# f_handler = open('out.log','w')
# sys.stdout = f_handler
#加入断点续存功能
#加入分布式爬取功能


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
from multiprocessing import Pool

class lj_2sf:

    #初始化
    def __init__(self):

        #设置文件名
        self.csv_title = 'sh_lj_2s_pro_3.csv'

        #设置日志文件
        # self.log = open('sh_lj_2s_pro_3.log','a')
        self.log = 'sh_lj_2s_pro_3.log'

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

        #设置代理开关，默认打开
        self.proxy_control = True

        # 加入cookies
        self.enable_cookie = True
        # 设置cookie
        self.cookie = cookielib.LWPCookieJar()
        # cookie处理器
        self.cookie_handler = urllib2.HTTPCookieProcessor(self.cookie)

    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    # 获取当前时间
    def getCurrentDate(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # 设置一个能同时打印和输出日志的函数printlog
    # 参数1为需要输出的内容，参数2位日志保存的路径
    def printlog(self,msg, printcontrol = True):

        if printcontrol == True:
            time = self.getCurrentTime()
            # date = self.getCurrentDate()
            try:
                content = time + msg
                print content
                content = content.strip().encode('utf-8') + '\n'
                f = open(self.log, "a")
                f.write(content)
            except:
                print "printlog Error"
            # f.close()
        else:
            print(msg)
        # return None



    #建立IP代理池，从网页获取
    def getIPlist(self):
        start = time.clock()
        iplist = []  ##初始化一个list用来存放我们获取到的IP
        html = requests.get("http://haoip.cc/tiqu.htm")  ##不解释咯
        iplistn = re.findall(r'r/>(.*?)<b', html.text,
                             re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
        for ip in iplistn:
            i = re.sub('\n', '', ip)  ##re.sub 是re模块替换的方法，这儿表示将\n替换为空
            iplist.append(i.strip())  ##添加到我们上面初始化的list里面, i.strip()的意思是去掉字符串的空格哦！！（这都不知道的小哥儿基础不牢啊）
        # print(i.strip())
        # print(iplist)
        end = time.clock()
        t = end - start
        # print "getIPlist's time is " + str(t)
        self.printlog("getIPlist's time is " + str(t))
        return iplist


    #获取页面
    def getPage(self, url):
        start = time.clock()
        try:
            UA = random.choice(self.user_agent_list)
            # 从self.user_agent_list中随机取出一个字符串（聪明的小哥儿一定发现了这是完整的User-Agent中：后面的一半段）

            headers = {'User-Agent':UA}
            request = urllib2.Request(url, headers = headers)

            #设置代理
            if self.proxy_control == False:
                proxy_handler = urllib2.ProxyHandler({})
            else:
                proxy_handler = urllib2.ProxyHandler({"http": '%s'%self.IP})

            opener = urllib2.build_opener(proxy_handler, self.cookie_handler, urllib2.HTTPHandler)
            response = opener.open(request, timeout=3)
            content = response.read()

        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
                # self.printlog(e.code)
            if hasattr(e,"reason"):
                print e.reason
                # self.printlog(e.reason)
            else:
                # print "gePage is Wrong"
                self.printlog("gePage is Wrong")

    #     #链家居然不要解压也不需要解码，良心
    #     # print content
        end = time.clock()
        t = str(end-start)
        # print "getPage use time: "+t
        return content

        #获取行政区信息
    def getDistrict(self,url):
        # 打开代理
        self.proxy_control = False

        html = self.getPage(url)
        tree = lxml.html.fromstring(html)

        # 获取行政区列表
        try:
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
        except:
            # print "getDistricts Error"
            self.printlog("gePage is Wrong")

        #关闭代理
        self.proxy_conrol = True
        return datas

    #获取页面内容
    def getDatas(self,url):

        content = self.getPage(url)

        try:
            tree = lxml.html.fromstring(content)

            #把所有的li项目抽取出来
            items = tree.xpath('//div[@class="con-box"]/div[@class="list-wrap"]/ul[@id="house-lst"]/li')

            datas = []
            #单挑li的内容解析，获取房子信息:下层链接，标题，小区，户型,面积，楼层、朝向、建造时间，距离，满五,钥匙，总价，单价，查看人数
            #楼层、建造时间、装修、朝向、首付、月供、区域、地址
            self.item_i = 1
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
                datas.append([son_url, title, block, type, area, distance, tax, key, price, price_pre, num ,son_data[0], son_data[1], son_data[2], son_data[3], son_data[4], son_data[5], son_data[6],son_data[7], son_data[8],son_data[9],son_data[10],str(self.page_i),str(self.item_i)])


        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
                # self.printlog(e.code)
            if hasattr(e, "reason"):
                print e.reason
                # self.printlog(e.reason)
            else:
                # print "geDatas is Wrong"
                self.printlog("geDatas is Wrong")
        return datas

    #从子链接获取楼层、建造时间、装修、朝向、首付、月供、区域、地址
    def getSonDatas(self,url):

        content = self.getPage(url)

        try:
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
            month_pay = month_pay[1].strip() if month_pay else ' '
            # print month_pay
            #区域
            location = tree.xpath('//div[@class="esf-top"]/div[@class="cj-cun"]/div[@class="content"]/table//tr[5]//span[@class="areaEllipsis"]/text()')
            location = location[0].strip().split(' ') if location else ' '

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
            data = [floor,build_time,fitment,orientation,pre_pay,month_pay,location[0],location[1],address,last_deal,house_property]
            self.item_i += 1

        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
                # self.printlog(e.code)
            if hasattr(e, "reason"):
                print e.reason
                # self.printlog(e.reason)
            else:
                # print "geSonData is Wrong"
                self.printlog("getSonData is Wrong")
        # print datas
        return data


    #存储模块
    #CSV文件初始化
    def init_Csv(self):
        csvfile = open(self.csv_title, 'wb')
        writer = csv.writer(csvfile)
        writer.writerow(['具体链接','标题','小区','户型','面积','距离','满五','钥匙','总价','单价','查看人数',\
                         '楼层','建造时间','装修','朝向','首付','月供','行政区','区域','地址','上次交易','房屋类型','页码','条数'])
        csvfile.close()

    #保存到CSV
    def SaveCsv(self,url):

        datas = self.getDatas(url)

        #写入数据
        try:
            csvfile = open(self.csv_title, 'ab')
            writer = csv.writer(csvfile)

            for data in datas:
                csv_data = []
                for item in data:
                    item = item.strip().encode('utf-8')
                    csv_data.append(item)
                writer.writerow(csv_data)

            csvfile.close()
        except:
            # print "SaveCsv ERROR"
            self.printlog("SaveCsv ERROR")

    #获取某个区的所有信息
    def getDistrictDatas(self, district,csv_control = False):

        self.printcontrol = True

        if csv_control:
            self.init_Csv()

        self.iplist = self.getIPlist()
        self.IP = random.choice(self.iplist)
        self.printlog(self.IP)

        district = district
        i = 1
        while i < 101:
            try:
                self.page_i = i
                # url = "http://sh.lianjia.com/ershoufang/d"+str(i)
                # print "%s page %s is start crawling."%(district[0],str(i))
                self.printlog("%s page %s is start crawling." % (district[0], str(i)))

                # page_url = url[0:-1]+district+str(i)
                page_url = district[1] + "/d" + str(i)
                # print page_url
                self.printlog(page_url)
                # self.IP = self.getIP(url)
                # print "proxy IP: %s" % (self.IP)
                self.printlog("proxy IP: %s" % (self.IP))

                # datas = self.getDatas(url)
                self.SaveCsv(page_url)

                # csvfile = open(self.csv_title, 'ab')
                # writer = csv.writer(csvfile)
                # writer.writerow(['Page %s is finised' % (str(i))])
                # csvfile.close()

                # print "%s page %s is finished."%(district[0],str(i))
                self.printlog("%s page %s is finished." % (district[0], str(i)))
            except:
                # print "restart"
                self.printlog("restart")
                self.IP = random.choice(self.iplist)
                continue

            i += 1
        # print district[0]+" is written."
        self.printlog(district[0] + " is written.")

    #启动器
    def start(self,url,csv_control=False):

        self.printcontrol = True

         #是否初始化CSV
        if csv_control:
            self.init_Csv()

        self.iplist = self.getIPlist()
        self.IP = random.choice(self.iplist)
        # print self.IP
        self.printlog(self.IP)

        districts = self.getDistrict(url)
        # print districts
        # datas = []
        # for district in districts:
        #     datas.append(district)
        # print datas
        #开始多进程写入

        #开始写入:
        for district in districts:
            self.getDistrictDatas(district)

            # i = 1
            # while i < 101:
            #     try:
            #
            #         # url = "http://sh.lianjia.com/ershoufang/d"+str(i)
            #         # print "%s page %s is start crawling."%(district[0],str(i))
            #         self.printlog("%s page %s is start crawling." % (district[0], str(i)))
            #
            #         # page_url = url[0:-1]+district+str(i)
            #         page_url = district[1]+"/d"+str(i)
            #         # print page_url
            #         self.printlog(page_url)
            #         # self.IP = self.getIP(url)
            #         # print "proxy IP: %s" % (self.IP)
            #         self.printlog("proxy IP: %s" % (self.IP))
            #
            #         # datas = self.getDatas(url)
            #         self.SaveCsv(page_url)
            #
            #         csvfile = open(self.csv_title, 'ab')
            #         writer = csv.writer(csvfile)
            #         writer.writerow(['Page %s is finised'%(str(i))])
            #         csvfile.close()
            #
            #         # print "%s page %s is finished."%(district[0],str(i))
            #         self.printlog("%s page %s is finished."%(district[0],str(i)))
            #     except:
            #         # print "restart"
            #         self.printlog("restart")
            #         self.IP = random.choice(iplist)
            #         continue
            #
            #     i += 1
            # # print district[0]+" is written."
            # self.printlog(district[0]+" is written.")
        # print "The porject of lianjia_ershoufang is finished"
        self.printlog("The porject of lianjia_ershoufang is finished")





# url = "http://sh.lianjia.com/ershoufang/d1"
# url1 = "http://sh.lianjia.com/ershoufang/sh4499373.html"
# test = lj_2sf()
# test.getDatas(url)
# test.init_Csv()
# test.getPageNum(url)
# test.start(url,True)
# test.getIPlist()

# datas = test.getDistrict(url)
# districts = []
# map(test.getDistrictDatas, datas)

# i=1
# district = 0
# test.printlog("%s page %s is start crawling."%(district,str(i)))
# test.printlog("hello world %s" % (i))

def getRun(district):
    getrun = lj_2sf()
    getrun.getDistrictDatas(district,True)

if __name__ == '__main__':

    run = lj_2sf()
    url = "http://sh.lianjia.com/ershoufang/d1"
    url1 = "http://sh.lianjia.com/ershoufang/sh4499373.html"

    start = time.clock()
    # run.start(url,True)

    districts = run.getDistrict(url)
    pool = Pool(processes=4)
    pool.map(getRun,districts)

    end = time.clock()
    t= str(end-start)
    run.printlog(t)

