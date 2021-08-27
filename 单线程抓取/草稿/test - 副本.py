import requests
from bs4 import BeautifulSoup
import lxml
import urllib
import urllib.parse
import os
import time


def GetImages(url):
    html = requests.get(url,timeout=(10)).content.decode("utf-8")
    soup = BeautifulSoup(html, 'lxml')
    imgs = soup.select("div.content div ul li a")
    for img in imgs:
        link = img['href']
        display=link.split('/')[-1]
        print('正在下载：',display)
        filename='./images/'+display
        urllib.request.urlretrieve(link,filename)
def GetUrls(page_links_list):
    pages = int(input("请输入你想爬取的页数："))
    if pages > 1:
        for page in range(2, pages + 1):
            url = "https://lolibooru.moe/post?tags=blush&page=" + str(page) + ".htm"
            page_links_list.append(url)
    else:
        page_links_list=page_links_list



if __name__ == '__main__':
    page_links_list=["https://lolibooru.moe/post?tags=blush"]
    GetUrls(page_links_list)
    os.mkdir('./images')
    print("开始下载图片！！！")
    start = time.time()
    for url in page_links_list:
        GetImages(url)
    print('图片下载成功！！！')
    end = time.time() - start
    print('消耗时间为：', end)

