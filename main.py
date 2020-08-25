#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "MiaoYan"
__email__ = "miaoy2018@lzu.edu.com"

#pip3 install lxml
#pip3 install ps4
#pip3 install selenium

########
import requests
import re
from urllib.parse import urlunsplit

def gethtml(url):
    headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
    }
    #req.status_code
    #req.text
    req=requests.get(url,headers=headers)
    return req.text

#url="https://httpbin.org/get"
path='www.malimalihome.net'
add='/residential'
language="lang=zh_CN"
begin="skipCount=0"
step="maxResultCount=20"
query=language+"&"+begin+"&"+step
scheme='https'
#?lang=zh_CN&skipCount=0&maxResultCount=10 #简体中文，从第一项开始且一页显示10项
url=urlunsplit([scheme,path+add,'',query,''])

html=gethtml(url)

#req.json

#from bs4 import BeautifulSoup
#data=req.text
#soup=BeautifulSoup(data,'lxml')
html=re.sub('<b>|</b>|<span.*?>|</span>| |\\r|\\n|&nbsp','',html)
pattern=re.compile(
    'list-cover.*?<img.*?src="(.*?)".*?<div.*?result-list-c-title.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?-c-type.*?>(.*?)</div>.*?-c-desc.*?>(.*?)<.*?-r-price.*?>(.*?)</div>'
    )
#re.S
items=re.findall(pattern,html)
print(items)
l=[]
for i in items:
    dic={}
    dic["房名"]=i[2]
    dic["照片"]=i[0]
    dic["描述"]=i[3]
    dic["其他"]=i[4]
    dic["价格"]=i[5]
    add=i[1]
    url=urlunsplit([scheme,path+add,'','',''])
    print(url)
    html=gethtml(url)
    html=re.sub('\\r|\\n|\\t|&nbsp','',html)
    pattern=re.compile(
    '<span.*?glyphicon-map-marker.*?/span>(.*?)</div>'
    )
    s=re.findall(pattern,html)[0]
    dic["地址"]=s
    print(s)
    l.append(dic)
    

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


import os
def create_file(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)

create_file('pictures')
save_path='pictures\\'
from urllib.request import urlopen
def save_picture(name='',url=''):
    f= open(name, 'wb')
    pic = urlopen(url)
    wri=pic.read()
    f.write(wri)
    pic.close()
    f.close()


def check_path(str=''):
    illi_l=['/','\\',':','?','*','"','<','>','|']
    for i in illi_l:
        str=str.replace(i,'')
    return str

for i in l:
    file_path=save_path+check_path(i['房名'])
    create_file(file_path)
    save_p=file_path+'\\1.jpg'
    save_picture(name=save_p,url=i['照片'])
    print(i['房名'])
