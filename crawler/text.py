#!/usr/bin/python
# _*_ coding:utf-8 _*_

import urllib
import urllib2
import chardet
import gzip
import StringIO

# url = 'http://land.fang.com'
# response = urllib2.urlopen(url)
# content = response.read()
# # print content.getcode()
# # print content.read().decode('gbk')
# # charset_info = chardet.detect(content)
# content = StringIO.StringIO(content)
# gzipper = gzip.GzipFile(fileobj=content)
# content = gzipper.read().decode('gbk')
# print content
# print charset_info

ip = '218.76.106.78:3128'
proxy_handler = urllib2.ProxyHandler({"http": ip})
opener = urllib2.build_opener(proxy_handler)
html = opener.open('http://sh.lianjia.com/ershoufang/d1')
content = html.read()
print html.getcode()
print content

