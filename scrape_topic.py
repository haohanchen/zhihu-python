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
This program scrape all answers under one topic

"""

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




def get_topic_pages(topic_id):
    urls = [] 
    for n_page in range(1, 33): # I make the page number given for now. Will write a function to find this out. it is the second last text of link in class "zm-invite-paper"
        urls.append( (r'https://www.zhihu.com/topic/' + str(topic_id) + r'/questions?page=' + str(n_page)) )
    return urls


def get_question_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    question_a = soup.findAll( True, {'class': 'question_link'} )
    links = []
    for a in question_a:
        links.append(a['href'])
        print a['href'], a.get_text()
    return links
    


def get_question_url_all(topic_id):
    print '\n======================\n======================'
    print termcolor.colored( ' '.join(['NOW ON TOPIC:', str(topic_id)]), 'red' )
    print '\n======================\n======================\n'    
    topic_urls = get_topic_pages(topic_id)    
    question_urls_all = []
    for page_url in topic_urls:
        print termcolor.colored('I am on Page: ', 'green'), termcolor.colored(page_url, 'magenta')
        question_urls_all.extend( get_question_url(page_url) )

        t_sleep = random.uniform(2,4) # Stop after scraping one page.
        print '==============END OF PAGE==============\n'
        print termcolor.colored(' '.join(['Sleep Time: ', str(t_sleep)]), "red")
        time.sleep(t_sleep)
    return question_urls_all                




def download_answers(urls, topic_id, log_fname):
    answer_file_name = "Answers_text_" + topic_id + ".txt"

    # Open a file to store all answers
    if not os.path.exists( os.path.join(os.getcwd(), answer_file_name) ):
        out_answer_text = open(answer_file_name, "w")
        out_answer_text.close()    
    
    for i in range(0, len(urls)):
        url = urls[i]
        print url
        question = Question('http://www.zhihu.com' + url)

        # 获取该问题的标题
        title = question.get_title()
        # 获取该问题的详细描述
        detail = question.get_detail()
        # 获取回答个数
        answers_num = question.get_answers_num()
        # 获取关注该问题的人数
#       try:
#           followers_num = question.get_followers_num()
#       except:
#           followers_num = 0
        # 获取该问题所属话题
        topics = question.get_topics()
        # 获取该问题被浏览次数
#       visit_times = question.get_visit_times()
        # 获取排名第一的回答
#       top_answer = question.get_top_answer()
        # 获取排名前十的十个回答
#       top_answers = question.get_top_i_answers(10)
        # 获取所有回答
        answers = question.get_all_answers()

        print "============"    
        print "问题: \n", title  
        print "问题描述: \n", detail
        print "Number of Answers: ", answers_num 
#       print followers_num
        for topic in topics:
            print topic, 
#       print visit_times 
#       print top_answer  
#       print top_answers  
        print answers 

        out_answer_text = open(answer_file_name, "a")        
        this_question_answers_text = []
        for answer in answers:
            author = answer.get_author()
            answer_cleaned = answer.text_one_line()
            print answer_cleaned
            
            this_question_answers_text.append(answer_cleaned)
#           answer.to_txt(title, detail, answers_num, followers_num, topics, visit_times, author)
#           t_sleep = random.uniform(2,4) # Stop after scraping one page.
#           print termcolor.colored(' '.join(['Sleep Time: ', str(t_sleep)]), "white")
#           time.sleep(t_sleep)
#           print "\n"            
        out_answer_text.write( "".join(this_question_answers_text) )

        # Modify log file after successfully write the answers
        log_file = open(log_fname, "w")
        log_file.write("\n".join(urls[i:]))
        print termcolor.colored("Log modified.", "white")
        # Stop after scraping one page.
        print "\n--------------\n--------------"
        t_sleep = random.uniform(1,2) 
        print termcolor.colored(' '.join(['Sleep Time: ', str(t_sleep)]), "red")
        time.sleep(t_sleep)
    out_answer_text.close()


# Get URLs to scrape either from log or by scraping the topic page.
def get_urls(topic_id, log_fname):
    if not os.path.exists( os.path.join(os.getcwd(), log_fname) ):
        print "Starting to generate log file...\n"
        # Scrape list of URLs
        urls = get_question_url_all(topic_id)
        # Write the log file
        log_file = open(log_fname, "w")
        log_file.write("\n".join(urls))
        log_file.write("\n")
        print termcolor.colored("Log file for this topic is successfully generated.", "green")
    else:
        print termcolor.colored("Log file for this topic already exists. \n Read URLs from Log File.", "white")
        urls = open( os.path.join(os.getcwd(), log_fname) ).read().split("\n")
    return urls
    

def main():
    topic_id = "19592892"
    log_fname = "ToScrape_topic_" + topic_id + ".txt"

     # Topic: 贫富差距 (Income Gap)
    urls = get_urls(topic_id, log_fname)
    for url in urls:
        print url

    download_answers(urls, topic_id, log_fname)


if __name__ == '__main__':
    main()