# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import os
import base64
import json
import requests
from threading import Thread
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
#创建浏览器对象

path_main='/'

browser = webdriver.Chrome(path_main+'bilibili/chromedriver',options=chrome_options)


imgpath=path_main+'download/img.jpg'
downpath=path_main+'download/'
cookies_path=path_main+'bilibili/data/cookies'
img_url_path=path_main+'bilibili/data/img_url'
img_url_done_path=path_main+'bilibili/data/img_url_done'
url_path=path_main+'bilibili/data/url'
url_done_path=path_main+'bilibili/data/url_done'



url_login='https://passport.bilibili.com/login'
url_t='https://t.bilibili.com/'


#main
def get_data():
    print('Th1_解析器启动')
    print('Th1_url初始化\n')
    with open(url_path,'w') as f_clear:
        f_clear.write('')
        f_clear.close()
    print('Th1_url初始化done\n')
    print('Th1_img_url初始化\n')
    with open(img_url_path,'w') as f_clear:
        f_clear.write('')
        f_clear.close()
    print('Th1_img_url初始化done\n')
    print('Th1_loading\n')
    get_login()
    print('Th1_loading_done\n')
    while True:
        browser.get(url_t)
        time.sleep(20)
        js="var q=document.documentElement.scrollTop=100000"
        browser.execute_script(js)
        time.sleep(20)
        cards=browser.find_elements_by_class_name('card')
        print("Th1_拿到card\n")
        url=[]
        for card in cards:
            try:
                data=card.find_element_by_class_name('video-container.can-hover')
                src=data.find_element_by_tag_name('a').get_attribute('href')
                if 'BV' in src:
                    url.append(src)
                    print("Th1_添加card\n")
            except BaseException:
                pass
        img_cards=browser.find_elements_by_class_name('img-content')
        img_url=[]
        print("Th1_拿到img_card\n")
        for img_card in img_cards:
            try:
                style=img_card.get_attribute('style')
                src=style.split('"',2)
                url_temp=src[1]
                src=url_temp.split('@',1)
                img_src=src[0]
                img_url.append(img_src)
                print("Th1_添加img_catd\n")
            except BaseException:
                pass

        print('Th1_查重中\n')    
        with open(url_path,'r') as f_2:
            data_old=f_2.read()
            f_2.close()
        with open(url_path,'a') as f_3:
            for url_1 in url:
                if url_1 in data_old:
                    pass
                else:
                    f_3.write(url_1+'\n')
            f_3.close()
        print('Th1_去重写入成功\n')
        print('Th1_img_url查重中\n')              
        with open(img_url_path,'r') as f_4:
            img_data_old=f_4.read()
            f_4.close()
        with open(img_url_path,'a') as f_5:
            for url_1 in img_url:
                if url_1 in img_data_old:
                    pass
                else:
                    f_5.write(url_1+'\n')
            f_5.close()
        print('Th1_img去重写入成功\n')
        print('Th1_200s等待\n')
        time.sleep(200)
        print('Th1_200s结束\n')

#main
def clear():
    print('Th2_下载器启动\n')
    time.sleep(120)
    print('Th2_下载器120等待结束')
    print('Th2_开始解析下载循环\n')
    while True:
        with open(img_url_path,'r')as f:
            img_urls_new=f.read()
            f.close()
        with open(img_url_done_path,'r')as f_done:
            img_url_done=f_done.read()
            f_done.close()
        print('Th2_读取img_url\n')
        img_urls_new=img_urls_new.split('\n')
        i=1
        for img_url in img_urls_new:
            if img_url in img_url_done:
                pass
            else:
                img_download(img_url)
                print('Th2_img已下载\n'+str(i))
                time.sleep(1)
                i=i+1
        print('Th2_img下载完成\n')
        with open(url_path,'r')as f:
            urls_new=f.read()
            f.close()
        with open(url_done_path,'r')as f_done:
            url_done=f_done.read()
            f_done.close()
        urls_new=urls_new.split('\n')
        i=1
        for url in urls_new:
            if url in url_done:
                pass
            else:
                print('Th2_视频已下载'+str(i))
                download(url)
                i=i+1
            time.sleep(2)


def get_login():
    if os.path.exists(cookies_path):
        pass
    else:
        get_cookies()
    browser.get(url_t)
    with open(cookies_path, 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        browser.add_cookie(cookie)
    time.sleep(5)


def get_cookies():
    browser.get(url_login)
    time.sleep(20)
    img_login=browser.find_element_by_class_name('qrcode-img').find_element_by_tag_name('img').get_attribute('src')
    get_login_b64decode(img_login)
    time.sleep(90)
    os.remove(imgpath)
    dictCookies=browser.get_cookies()
    jsonCookies = json.dumps(dictCookies)
    with open(cookies_path, 'w') as f:
        f.write(jsonCookies)
        f.close()


def get_login_b64decode(img_data):
    img_data=img_data.split(';',1)[1]
    img_data=img_data.split(',',1)[1]
    img_data_decode=base64.b64decode(img_data)
    with open(imgpath,'wb')as f:
        f.write(img_data_decode)
        f.close()


def download(url):
    os.system( "you-get -o "+downpath+'/video'+' '+url)
    with open(url_done_path,'a')as f:
        f.write(url+'\n')
        f.close()


def img_download(img_url):
    r = requests.get('https:'+img_url)
    with open(downpath+'img/'+str(int(time.time()))+'.jpg', 'wb') as f:
        f.write(r.content)
    with open(img_url_done_path,'a')as f:
        f.write(img_url+'\n')
        f.close()

thread_01 = Thread(target=get_data)
thread_02=Thread(target=clear)
thread_01.start()
thread_02.start()
