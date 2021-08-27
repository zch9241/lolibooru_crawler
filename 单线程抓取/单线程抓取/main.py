# Authors: 小蜗牛 <2426936965@qq.com><https://github.com/zch9241>
# 


from bs4 import BeautifulSoup
import lxml
import os
import requests
import time
import urllib
import urllib.parse


import Custom_Function as fun


if __name__ == '__main__':
    print("这是 main.py ,程序已开始运行！")

    page_links_list=['https://lolibooru.moe/post?tags=blush']
    #page_links_list=[str(input("请输入要抓取的网址："))]

    fun.GetUrls(page_links_list)
    os.mkdir('./images')
    print("开始下载图片！！！")
    start = time.time()
    for url in page_links_list:
        fun.Get_Images_Encode_Urls(url)
    print('图片下载成功！！！')
    end = time.time() - start
    print('消耗时间为：', end,'s')
