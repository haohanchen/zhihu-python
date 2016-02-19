# -*- coding: utf-8 -*-

from zhihu import Question
from zhihu import Answer
from zhihu import User
from zhihu import Collection

# Build-in / Std
import os, sys, time, platform, random
import re, json, cookielib
import codecs

# requirements
import requests, termcolor
from bs4 import BeautifulSoup

# module
from auth import islogin
from auth import Logging


"""
    Note:
        1. 身份验证由 `auth.py` 完成。
        2. 身份信息保存在当前目录的 `cookies` 文件中。
        3. `requests` 对象可以直接使用，身份信息已经自动加载。

    By Luozijun (https://github.com/LuoZijun), 09/09 2015

"""
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
try:
    requests.cookies.load(ignore_discard=True)
except:
    Logging.error(u"你还没有登录知乎哦 ...")
    Logging.info(u"执行 `python auth.py` 即可以完成登录。")
    raise Exception("无权限(403)")


if islogin() != True:
    Logging.error(u"你的身份信息已经失效，请重新生成身份信息( `python auth.py` )。")
    raise Exception("无权限(403)")


# All above are from zhihu.py
# These are essential, but I do not know why yet. 
# Important: requests.Session(), requests.cookies, requests.cookies.load(ignore_discard=True)


url = r'https://www.zhihu.com/topic/19592892/questions?page1'

links = []
r = requests.get(url)
soup = BeautifulSoup(r.content)
question_a = soup.findAll( True, {'class': 'question_link'} )


for a in question_a:
    links.append(a['href'])

for link in links:
    print link


#question = Question('https://www.zhihu.com/question/27934825')
#print question.get_title()