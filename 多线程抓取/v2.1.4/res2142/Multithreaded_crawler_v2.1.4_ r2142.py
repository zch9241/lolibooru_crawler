# Author: 小蜗牛 <2426936965@qq.com><https://github.com/zch9241>
# 
# 版权声明：该 .py 文件是「zch」的原创代码，转载请附上本声明。
# 
# Version: 2.1.4
# Release: 2142
# 
# 版本更新说明：
# v1.0 程序首个版本
# v2.0 由单线程爬取转为多线程爬取
# v2.1 修复了爬取过程中图片重复下载的问题（Pr.1）
# v2.1.1 交互性提升；优化使用体验；代码优化（无需二次编码）
# v2.1.2 增加了查询页面总页数的功能
# v2.1.3 修复了查询页面总页数时出现的无效字符（Pr.2）；代码优化（转移到"if __name__ == '__main__':"中）
# v2.1.4 修复了当页面数量较少时查询页面总页数的报错（Pr.3）；修复了图片下载不完整的问题（Pr.4）
# 
# Problem : 01 - in (class)    Producer run
# Problem : 02 - in (function) Getlastpage ("..."+lastpage)<...为无效字符>
# Problem : 03 - in (function) Getlastpage ("[n]")<n的值有误>
# Problem : 04 - in (variable) headers
# 


from bs4 import BeautifulSoup
import os
import re
import requests
import threading
import time
import urllib
import urllib.parse



print("这是 Multithreaded_crawler.py ,程序开始运行！")

imglist = []    #最终图片存储列表
links = []       #页面翻页链接列表


headers = {
    "Host": "https://lolibooru.moe/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0"
}


def Getlastpage():
    html = requests.get(page_links_list[0],timeout=(10000)).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    alllink = soup.select("body div#content div#post-list div.content div#paginator div.pagination a")

    for linkper in alllink:
        link_per = linkper['href']
        link_per_pro = urllib.parse.unquote(link_per)
        link_per_pro_final = re.findall(r"\d+\.?\d*",link_per_pro)
        links.append(link_per_pro_final)

    length = len(links)
    digit = length - 2

    last_page_number = links[digit]    #末页所在列表元素

    return last_page_number


def GetUrls(page_links_list):
    pages = int(input("请输入你想爬取的页数："))

    if pages > 1:
        for page in range(2, pages + 1):
            url = "https://lolibooru.moe/post?tags=" + str(key_pro) +"&page="+ str(page) + ".htm"
            page_links_list.append(url)
    else:
        page_links_list=page_links_list

#初始化锁,创建一把锁
gLock=threading.Lock()
 
#生产者，负责从每个页面中获取图片的链接
class Producer(threading.Thread):
    def run(self):
        #----url整合空列表----
        img_link = []
        img_links = []
        img_encode_links_pro = []
        #最终的图片url列表在 Geturls 前

        #----url整合空列表----
        
        while len(page_links_list)>0:
            #上锁
            gLock.acquire()
            
            p = len(page_links_list)

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
            
                num = len(img_link)

                for w in range(1, num+1, 2):        #过滤无效链接
                    img_links.append(img_link[w])

                numb = len(img_links)

                for q in range(1, numb+1):          #编码
                    img_encode_link = urllib.parse.quote(img_links[q-1], safe=":/=?#")
                    img_encode_links_pro.append(img_encode_link)

                numbers = len(img_encode_links_pro)

                for a in range(1,numbers+1):       #将每次循环中所得到的的链接存入汇总
                    imglist.append(img_encode_links_pro[a-1])

                print('链接整合中！','   ', '已完成：', i+1, '共有：', p)

                img_link = []
                img_links = []
                img_encode_links_pro = []

            print('链接已整合！')
            print('3秒后开始下载！')
            time.sleep(3)
            
            #释放锁
            gLock.release()


#消费者，负责从获取的图片链接中下载图片
class Consumer(threading.Thread,):
    def run(self):
        print("%s is running"%threading.current_thread())
        while True:
            #print(len(imglist))
            #上锁
            gLock.acquire()

            if len(imglist)==0:
                #不管什么情况，都要释放锁
                gLock.release()
                continue
            else:
                img_url=imglist.pop()

                leng = len(imglist)
                
                print(".")
                print(".")
                print(".")
                print(".")
                print('未下载：', leng)
                print(".")
                print(".")
                print(".")
                print(".")
                
                gLock.release()
                
                filename=img_url.split('/')[-1]
                print('正在下载：', filename)
                path = './images/'+filename
                urllib.request.urlretrieve(img_url, filename=path)
                if len(imglist)==0:
                    end=time.time()
                    print("消耗的时间为：", (end - start), "秒")
                    exit()
 


if __name__ == '__main__':
    # -------------页面链接的初始化列表-------------
    #page_links_list=["https://lolibooru.moe/post?tags=mochiyuki"]
    #page_links_list=["https://lolibooru.moe/post?tags=blush"]

    page_links_list=[str(input("请输入要抓取的网址："))]

    last_page_number_pro = Getlastpage()

    print("（总共",last_page_number_pro,"页）")

    key=str(page_links_list[0])
    key_pro=key[32:]    #字符串切片得到关键词

    # -------------页面链接的初始化列表-------------
    GetUrls(page_links_list)

    folder = str(input('请输入要存储的文件夹（直接回车则使用默认 images）：'))

    if folder == '':
        folder = 'images'

    Folder = './' + folder

    os.mkdir(Folder)

    start=time.time()
    # 1个生产者线程，去从页面中爬取图片链接
    for x in range(1):
        Producer().start()
 
    # 10个消费者线程，去从页面中提取下载链接，然后下载
    for x in range(10):
        Consumer().start()
