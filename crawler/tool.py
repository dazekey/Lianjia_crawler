#!/usr/bin/python
# encoding: utf-8

"""
@author: ocean
@contact: dazekey@163.com
@file:Tool.py
@time:2017/2/20 22:28
"""

import re

#处理页面标签类
class Tool:
    #去除img标签，7位长空格，| 或（并）的意思， 7{7}匹配7个7
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接的标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换位\n
    replaceLine = re.compile('<tr>|<div>|<div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    #将段落开头换位\n加空两个
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签删除
    replaceExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.replaceExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()