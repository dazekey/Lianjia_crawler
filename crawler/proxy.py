# _*_ coding:utf-8 _*_
import re
import requests
import urllib2
import time

class getProxyIP:

    #从网站获取proxy_ip地址
    def getIPlist(self):
        start = time.clock()
        iplist = [] ##初始化一个list用来存放我们获取到的IP
        html = requests.get("http://haoip.cc/tiqu.htm")##不解释咯
        iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S) ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
        for ip in iplistn:
            i = re.sub('\n', '', ip)##re.sub 是re模块替换的方法，这儿表示将\n替换为空
            iplist.append(i.strip()) ##添加到我们上面初始化的list里面, i.strip()的意思是去掉字符串的空格哦！！（这都不知道的小哥儿基础不牢啊）
        # print(i.strip())
        # print(iplist)
        end = time.clock()
        t = end-start
        print "getIPlist's time is "+str(t)
        return iplist

    #测试ip是否可以用
    def testIP(self,url):

        iplist = self.getIPlist()
        IPpool = []
        for ip in iplist:
            start = time.clock()
            ip ='%s'%str(ip.strip())
            proxy_handler = urllib2.ProxyHandler({"http": ip})
            opener = urllib2.build_opener(proxy_handler)
            try:
                html = opener.open(url,timeout=3)
                # print html.getcode()
                IPpool.append(ip)
            except Exception,e:
                print ip+" is failed."
                end = time.clock()
                t = str(end - start)
                print "use time: "+t
                continue
            # print ip, type(ip)

            print ip+" is useful."
            end = time.clock()
            t = str(end - start)
            print "use time: " + t
        # print IPpool

        return IPpool

    #存储可用的IPlist
    def saveIP(self,url):
        IPlist = self.testIP(url)
        f = open('IPlist.txt',"w")

        for ip in IPlist:
            f.write(ip+",")

        f.close()
        print "IPlist has been saved."
    #启动
    def start(self,url):
        self.saveIP(url)



url = "http://sh.lianjia.com/ershoufang/d1"
test = getProxyIP()
test.start(url)