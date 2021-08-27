from bs4 import BeautifulSoup
import lxml
import os
import requests
import threading
import time
import urllib
import urllib.parse



print("这是 Multithreaded_crawler.py ,程序开始运行！")

# -------------页面链接的初始化列表--------------
#page_links_list=["https://lolibooru.moe/post?tags=mochiyuki"]
#page_links_list=["https://lolibooru.moe/post?tags=blush"]

page_links_list=[str(input("链接："))]

pages = int(input("请输入你想爬取的页数："))

def GetUrls(page_links_list):
    global pages
    if pages > 1:
        key=str(page_links_list[0])
        key_pro=key[32:]    #字符串切片得到关键词
        for page in range(2, pages + 1):
            url = "https://lolibooru.moe/post?tags=" + str(key_pro) +"&page="+ str(page) + ".htm"
            page_links_list.append(url)
    else:
        page_links_list=page_links_list
        print(page_links_list)
links = []
def x():
    html = requests.get(page_links_list[0],timeout=(10000)).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    imgs = soup.select("body div#content div#post-list div.content div#paginator div.pagination a")

    for img in imgs:
        link = img['href']
        links.append(link)
        
GetUrls(page_links_list)
x()
print(links)
