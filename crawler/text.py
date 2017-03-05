#!/usr/bin/python
# _*_ coding:utf-8 _*_

import urllib
import urllib2
import chardet
import gzip
import StringIO

url = 'http://land.fang.com'
response = urllib2.urlopen(url)
content = response.read()
# print content.getcode()
# print content.read().decode('gbk')
# charset_info = chardet.detect(content)
content = StringIO.StringIO(content)
gzipper = gzip.GzipFile(fileobj=content)
content = gzipper.read().decode('gbk')
print content
# print charset_info
