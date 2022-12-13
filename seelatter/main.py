# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import os
import base64
import json
from threading import Thread
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
#创建浏览器对象

#path_main="/"
path_main='D:/backdata/'

#browser = webdriver.Chrome(path_main+'bilibili/chromedriver',options=chrome_options)
browser = webdriver.Chrome(path_main+'bilibili/chromedriver.exe',options=chrome_options)

imgpath=path_main+'bilibili/img.png'
cookies_path=path_main+'bilibili/data/cookies'
url_path=path_main+'bilibili/data/url'



url_login='https://passport.bilibili.com/login'
url_t='https://t.bilibili.com/'


#main
def get_data():
    print('解析器启动')
    print('url初始化\n')
    with open(url_path,'a+') as f_clear:
        f_clear.write('')
        f_clear.close()
    print('url初始化done\n')
    print('loading\n')
    get_login()
    print('loading_done\n')
    while True:
        browser.get(url_t)
        time.sleep(2)
        js="var q=document.documentElement.scrollTop=100000"
        browser.execute_script(js)
        time.sleep(2)
        js="var q=document.documentElement.scrollTop=100000"
        browser.execute_script(js)
        time.sleep(2)
        cards=browser.find_elements_by_class_name('card')
        print("拿到card\n")
        url=[]
        for card in cards:
            try:
                with open(url_path,'r') as f_2:
                    data_old=f_2.read()
                    print(data_old)
                    data_url=data_old.split('\n')
                    data=card.find_element_by_class_name('video-container.can-hover')
                    src=data.find_element_by_tag_name('a').get_attribute('href')
                    if 'BV' in src:
                        print('查重中\n')    
                        if src in data_url:
                            pass
                        else:
                            data.find_element_by_class_name('see-later').click()
                            with open(url_path,'a') as f_2:
                                f_2.write(src+'\n')
            except BaseException:
                pass
        print('120s等待\n')
        time.sleep(120)


def get_login():
    if os.path.exists(cookies_path):
        pass
    else:
        get_cookies()
    browser.get('https://www.bilibili.com')
    time.sleep(5)
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



if __name__=="__main__":
    get_data()