# Authors: 小蜗牛 <2426936965@qq.com><https://github.com/zch9241>
# 
# Version 2.0
#
# 版本更新说明：由单线程爬取转为多线程爬取


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
#----url整合空列表----
img_link = []
img_links = []
img_encode_links = []
#最终的图片url列表
img_encode_links_pro = []
#----url整合空列表----

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def GetUrls(page_links_list):
    pages = int(input("请输入你想爬取的页数："))
    if pages > 1:
        for page in range(2, pages + 1):
            url = "https://lolibooru.moe/post?tags=blush&page=" + str(page) + ".htm"
            page_links_list.append(url)
    else:
        page_links_list=page_links_list

#初始化锁,创建一把锁
gLock=threading.Lock()
 
#生产者，负责从每个页面中获取图片的链接
class Producer(threading.Thread):
    def run(self):
        while len(page_links_list)>0:
            #上锁
            gLock.acquire()
            #默认取出列表中的最后一个元素
            page_url=page_links_list.pop()
            #释放锁
            gLock.release()
 
            #获取img标签
            html = requests.get(page_url,headers=headers,timeout=(10000)).content.decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            imgs = soup.select("div.content div ul li a")

            #加锁3
            gLock.acquire()
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

            print('链接已整合！')
            
            #释放锁
            gLock.release()

 
#消费者，负责从获取的图片链接中下载图片
class Consumer(threading.Thread,):
    def run(self):
        print("%s is running"%threading.current_thread())
        while True:
            #print(len(img_encode_links_pro))
            #上锁
            gLock.acquire()
            
            if len(img_encode_links_pro)==0:
                #不管什么情况，都要释放锁
                gLock.release()
                continue
            else:
                img_url=img_encode_links_pro.pop()
                #print(img_encode_links_pro)
                gLock.release()
                filename=img_url.split('/')[-1]
                print('正在下载：', filename)
                path = './images/'+filename
                urllib.request.urlretrieve(img_url, filename=path)
                if len(img_encode_links_pro)==0:
                    end=time.time()
                    print("消耗的时间为：", (end - start))
                    exit()
 


if __name__ == '__main__':
    print("这是 Multithreaded_crawler.py ,程序开始运行！")
    GetUrls(page_links_list)
    os.mkdir('./images')
    start=time.time()
    # 5个生产者线程，去从页面中爬取图片链接
    for x in range(1):
        Producer().start()
 
    # 10个消费者线程，去从页面中提取下载链接，然后下载
    for x in range(5):
        Consumer().start()
