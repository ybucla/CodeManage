#!/usr/bin/python
# coding=utf-8

## 打开浏览器的方法
import webbrowser 
webbrowser.open('www.baidu.com') 

chromePath = r'你的浏览器目录'            #  例如我的：C:\***\***\***\***\Google\Chrome\Application\chrome.exe 
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))  #这里的'chrome'可以用其它任意名字，如chrome111，这里将想打开的浏览器保存到'chrome'
webbrowser.get('chrome').open('www.baidu.com'，new=1,autoraise=True)
## 

## ls dir
import os
print os.listdir("/media/cdrom0")
##

## upper 转大写
s.upper()
##

## 列表推导式
input = ['a','b','c','d','a']
filter = [x*3 for x in input if x == 'a'] # 等于a 的元素重复三次作为新列表元素
dict = [(i,input[i]) for i in range(len(input))]
##

## count non zero by row
import numpy as np

a = np.array([[1, 0, 1],
              [2, 3, 4],
              [0, 0, 7]])

columns = (a != 0).sum(0)
rows    = (a != 0).sum(1)
##
