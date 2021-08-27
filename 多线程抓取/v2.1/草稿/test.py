from bs4 import BeautifulSoup
import lxml
import os
import requests
import threading
import time
import urllib
import urllib.parse



# 页面链接的初始化列表
page_links_list=["https://lolibooru.moe/post?tags=blush"]
#page_links_list=[str(input("请输入要抓取的网址："))]
#----url整合空列表----
img_link = []
img_links = []
img_encode_links = []
#最终的图片url列表
img_encode_links_pro = []
#----url整合空列表----

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
pages = int(input("请输入你想爬取的页数："))
def GetUrls(page_links_list):
    global pages
    if pages > 1:
        for page in range(2, pages + 1):
            url = "https://lolibooru.moe/post?tags=blush&page=" + str(page) + ".htm"
            page_links_list.append(url)
    else:
        page_links_list=page_links_list

#初始化锁,创建一把锁
gLock=threading.Lock()
 
#生产者，负责从每个页面中获取图片的链接

def run():
    #----url整合空列表----
    img_link = []
    img_links = []
    img_encode_links = []
    imglist = []
    #最终的图片url列表
    img_encode_links_pro = []
    while len(page_links_list)>0:
        p=len(page_links_list)


        for i in range(p):
            #默认取出列表中的最后一个元素
            page_url=page_links_list.pop()



            #获取img标签
            html = requests.get(page_url,headers=headers,timeout=(10000)).content.decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            imgs = soup.select("div.content div ul li a")


            for img in imgs:                    #链接获得
                link = img['href']
                img_link.append(link)

            print('已获得链接！')
                
            num = len(img_link)

            for i in range(1, num+1, 2):        #过滤无效链接
                img_links.append(img_link[i])

            print('已获得有效链接！')

            numb = len(img_links)

            for q in range(1, numb+1):          #编码
                img_encode_link = urllib.parse.quote(img_links[q-1])
                img_encode_links.append(img_encode_link)

            print('链接已编码！')

            number = len(img_encode_links)

            for r in range(1,number+1):         #将https%3A//......改为可被识别的https://......
                img_per = img_encode_links[r-1]
                img_per = img_per.replace('%3A',':')
                img_encode_links_pro.append(img_per)

            numbers = len(img_encode_links_pro)

            for a in range(1, numbers+1):
                imglist.append(img_encode_links_pro[a-1])
            
            print("1",len(img_encode_links_pro))
            
            img_link = []
            img_links = []
            img_encode_links = []
            img_encode_links_pro = []

            print('链接已整合！')
            print("2",len(img_encode_links_pro))
            print(len(imglist))


GetUrls(page_links_list)
run()
