# _*_ coding:utf-8 _*_
import re
import requests

iplist = [] ##初始化一个list用来存放我们获取到的IP
html = requests.get("http://haoip.cc/tiqu.htm")##不解释咯
iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S) ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
for ip in iplistn:
    i = re.sub('\n', '', ip)##re.sub 是re模块替换的方法，这儿表示将\n替换为空
    iplist.append(i.strip()) ##添加到我们上面初始化的list里面, i.strip()的意思是去掉字符串的空格哦！！（这都不知道的小哥儿基础不牢啊）
# print(i.strip())
# print(iplist)

#测试ip是否可以用
for ip in iplist:
    ip ='%s'%str(ip.strip())
    print ip,type(ip)
