import requests
from bs4 import BeautifulSoup
import lxml
import urllib
import urllib.parse


def Get_Images_Encode_Urls(url):
    html = requests.get(url,timeout=(10000)).content.decode("utf-8")
    soup = BeautifulSoup(html, 'lxml')
    imgs = soup.select("div.content div ul li a")

    img_link = []
    img_links = []
    img_encode_links = []
    img_encode_links_pro = []

    for img in imgs:                          #链接获得
        link = img['href']
        img_link.append(link)

    print('已获得链接！')

    num = len(img_link)

    for i in range(1, num+1, 2):         #过滤无效链接
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

    numbers = len(img_encode_links)

    for s in range(1,numbers+1):
        links_per = img_encode_links_pro[s-1]
        display = links_per.split('/')[-1]
        print('正在下载：',display)
        filename='./images/'+display
        urllib.request.urlretrieve(links_per,filename)



def GetUrls(page_links_list):
    pages = int(input("请输入你想爬取的页数："))
    if pages > 1:
        for page in range(2, pages + 1):
            url = "https://lolibooru.moe/post?tags=blush&page=" + str(page) + ".htm"
            page_links_list.append(url)
    else:
        page_links_list=page_links_list

