import requests
from bs4 import BeautifulSoup
import lxml
import urllib
import os
def GetImages(url):
    img_links_list = []
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    imgs = soup.select("div.content div ul li a")
    for img in imgs:
        img_link = img['href']
        img_links_list.append(img_link)
        print()####

del img_links_list[0]

url="https://lolibooru.moe/post?tags=blush"


os.mkdir("./images")
print("下载开始！")

print(img_links_list)
print(len(img_links_list))
