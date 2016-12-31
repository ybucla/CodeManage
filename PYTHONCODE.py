#!/usr/bin/python
# coding=utf-8

## 打开浏览器的方法
import webbrowser 
webbrowser.open('www.baidu.com') 

chromePath = r'你的浏览器目录'            #  例如我的：C:\***\***\***\***\Google\Chrome\Application\chrome.exe 
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))  #这里的'chrome'可以用其它任意名字，如chrome111，这里将想打开的浏览器保存到'chrome'
webbrowser.get('chrome').open('www.baidu.com'，new=1,autoraise=True)
## 

