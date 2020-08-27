#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "MiaoYan"
__email__ = "miaoy2018@lzu.edu.com"

#pip3 install requests
#pip3 install re
#pip3 install csv
#然后安装urllib之类的库

########
import requests
import re
from urllib.parse import urlunsplit

l=[]

import os
from urllib.request import urlopen

def save_picture(name='',url=''):
    if not os.path.exists(name):
        try:
            f= open(name, 'wb')
            pic = urlopen(url,timeout=5)
            wri=pic.read()
            f.write(wri)
            pic.close()
            f.close()
        except Exception as e:
            print(e)
            pass
    else:
        print('已存在文件:',name)

def check_path(str=''):
    illi_l=['/','\\',':','?','*','"','<','>','|']
    for i in illi_l:
        str=str.replace(i,'')
    return str

def create_file(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    else:
        print('已存在文件:',file_path)

def gethtml(url):
    headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
    }#firefox浏览器表头
    req=requests.get(url,headers=headers,timeout=10)
    print("加载成功:",url)
    return req.text

def get_onepage_html(be=0,st=30,l_before=[]):
    #url="https://httpbin.org/get"
    path='www.malimalihome.net'
    add='/residential'
    language="lang=zh_CN"
    begin="skipCount="+str(be)#时间由近到远，从第0项开始爬
    step="maxResultCount="+str(st)#一次爬取多少个结果，30个。可选值10，20，30
    query=language+"&"+begin+"&"+step
    scheme='https'
    #?lang=zh_CN&skipCount=0&maxResultCount=10 #简体中文，从第一项开始且一页显示10项
    url=urlunsplit([scheme,path+add,'',query,''])#目标网页链接,拼接
    html=gethtml(url)#得到网页源码
    html=re.sub('<b>|</b>|<span.*?>|</span>| |\\r|\\n|&nbsp|;','',html)#去掉这些东西，方便查找
    pattern=re.compile(
        'list-cover.*?<img.*?src="(.*?)".*?<div.*?result-list-c-title.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?-c-type.*?>(.*?)</div>.*?-c-desc.*?>(.*?)<.*?-r-price.*?>(.*?)</div>'
        )#正则表达式
    #re.S#换行相关
    items=re.findall(pattern,html)
    print(items)
    add_l=[]#修改为list套dic的样式
    for i in items:
        dic={}
        dic["房名"]=i[2]
        add=i[1]
        url=urlunsplit([scheme,path+add,'','',''])
        print(url)
        html=gethtml(url)
        html=re.sub('\\r|\\n|\\t|&nbsp| ','',html)
        pattern=re.compile(
        '<span.*?glyphicon-map-marker.*?/span>(.*?)</div>'
        )
        s=re.findall(pattern,html)[0]
        dic["地址"]=s
        print(s)
        dic["照片"]=i[0]
        dic["描述"]=i[3]
        dic["其他"]=i[4]
        dic["价格"]=i[5]
        if dic in l_before:
            break
        add_l.append(dic)
    return add_l

#程序开始,爬取网页
#第一次爬取/初始化l
add_l=get_onepage_html()
for i in add_l:
    l.append(i)

#保存图片
def save_pictures(l=[]):
    create_file('pictures')
    save_path='pictures\\'
    for i in l:
        file_path=save_path+check_path(i['房名'])
        create_file(file_path)
        save_p=file_path+'\\封面.jpg'
        save_picture(name=save_p,url=i['照片'])
        print(i['房名'])

save_pictures(l)
#类似队列
#数据保存到csv文件中
import csv
headers=['房名','地址','照片','描述','其他','价格']
#w覆盖,a追加,一般我用a+
with open('test.csv', 'w',newline='',encoding = 'gb18030')as f:
    f_csv = csv.DictWriter(f,headers)
    f_csv.writeheader()
    for i in l:
        try:
            f_csv.writerow(i)
        except Exception as e:
            print(e)
            pass

def save_csv(l=[]):
    with open('test.csv', 'a+',newline='',encoding = 'gb18030')as f:
        f_csv = csv.writer(f)
        for i in l:
            try:
                f_csv.writerow(i)
            except Exception as e:
                print(e)
                pass

#save_csv(l,headers)#l是内容,headers题头
import time
while True:
    print("间歇三分钟")
    time.sleep(60*3)
    try:
        add_l=get_onepage_html(0,20,l_before=l)
        save_pictures(add_l)
        save_csv(add_l)
        lenth=len(l)-len(add_l)
        for i in range(lenth):
            add_l.append(l[i])
        l=add_l
        #l长度要比add大
    except Exception as e:
        print(e)
        pass