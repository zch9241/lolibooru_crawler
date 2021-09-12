# Author: 小蜗牛 <2426936965@qq.com><https://github.com/zch9241>
# 
# 版权声明：该软件（Mutithreaded_crawler）是「zch」的原创代码，转载请附上本声明。
# 
# Version: 2.2
# Release: 2203
# 
# 版本更新说明：
# v1.0 程序首个版本
# v2.0 由单线程爬取转为多线程爬取
# v2.1 修复了爬取过程中图片重复下载的问题（Pr.1）
# v2.1.1 交互性提升，优化使用体验；代码优化（无需二次编码）
# v2.1.2 增加了查询页面总页数的功能
# v2.1.3 修复了查询页面总页数时出现的无效字符（Pr.2）；代码优化（转移到"if __name__ == '__main__':"中）
# v2.1.4 修复了当页面数量较少时查询页面总页数的报错（Pr.3）；修复了图片下载不完整的问题（Pr.4）
# v2.1.5 交互性提升，优化使用体验；再次修复了图片下载不完整的问题（Pr.5）
# v2.2 交互性提升，优化使用体验；第三次修复了图片下载不完全的问题（Pr.6），此次修改规模较大
# 
# Problem : 01 - in (class)    Producer run
# Problem : 02 - in (function) Getlastpage ("..."+lastpage)<...为无效字符>
# Problem : 03 - in (function) Getlastpage ("[n]")<n的值有误>
# Problem : 04 - in (variable) headers <修改请求头>
# Problem : 05 - in (variable) headers <修改请求头>
# Problem : 06 - None <通过比较远程服务器的文件大小和本地文件大小判断图片下载是否完整，并触发修正机制>
#                None <当上述机制触发时，增加了断联后尝试恢复的机制><Urlopen Error [WINerror 10060]由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。>
# 


from bs4 import BeautifulSoup
import logging
import os
import re
import requests
import threading
import time
import urllib.request
import urllib.parse


#示例链接：
#page_links_list=["https://lolibooru.moe/post?tags=mochiyuki"]
#page_links_list=["https://lolibooru.moe/post?tags=blush"]

print("这是 Multithreaded_crawler.py ,程序开始运行！")

imglist = []     #最终图片存储列表
links = []       #页面翻页链接列表
errorlist = []   #下载不完整的图片列表


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "lolibooru.moe",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
#headers = {
#    "Host": "https://lolibooru.moe/",
#    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0",
#    "Accept": "*/*",
#    "Connection": "keep-alive",
#}


def Getlastpage():
    print('正在获取网页末页，请稍后...')
    print('这可能会花费大约10秒...')

    html = requests.get(page_links_list[0],headers=headers,timeout=(10000)).content.decode('utf-8')
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


def File_Exception_ErrorRaise():
    """
    触发因文件下载不完整的自定义错误
    """
    raise File_Exception

def Urlopen_Error_ErrorRaise():
    """
    触发因服务器关闭线程导致的自定义错误
    Urlopen Error [WINerror 10060]由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。
    """
    raise Urlopen_Error_Exception

class File_Exception(Exception):
    def __init__(self, err = '******Error: File_Exception: 文件下载不完整！******'):
        Exception.__init__(self,err)

class Urlopen_Error_Exception(Exception):
    def __init__(self, err = '******Error: Urlopen_Error_Exception:由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。******'):
        Exception.__init__(self,err)

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

                print('链接整合中！','   ', '已完成：', i+1, '  ','共有：', p)

                img_link = []
                img_links = []
                img_encode_links_pro = []

            print('链接已整合！')
            print('提示：下载图片保存在软件同目录下。')
            print('链接总长度（图片总数）：', len(imglist))
            print('5秒后开始下载！')
            time.sleep(5)
            
            #释放锁
            gLock.release()


#消费者，负责从获取的图片链接中下载图片
class Consumer(threading.Thread, File_Exception, Urlopen_Error_Exception):

    def __init__(self, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
 
    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞
 
    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞
 
    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False

#    def run(self):
#        while self.__running.isSet():
#            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到self.__flag为True后返回
#            print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#            time.sleep(1)

    def run(self):
        global folder
        global errorlist
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到self.__flag为True后返回
            print("running thread {}".format(threading.current_thread()))
            #上锁
            gLock.acquire()

            if len(imglist)==0:
                #不管什么情况，都要释放锁
                gLock.release()
                continue
            else:
                img_url=imglist.pop()

                leng = len(imglist)
                
                gLock.release()

                filename=img_url.split('/')[-1]

                RemoteFileSize = Consumer.getRemoteFileSize(self, url = img_url)

                print('未下载：', leng,'正在下载：', filename)
                path = './' + str(folder) + '/' + filename

                try:
                    try:
                        #下载图片
                        urllib.request.urlretrieve(img_url, filename=path)
                    except Urlopen_Error_Exception:
                        #winerror 10060
                        maxTryNum=10

                        print('尝试恢复连接...', maxTryNum)
                        for tries in range(maxTryNum):
                            try:
                                html = requests.get(page_links_list[0],headers=headers,timeout=(10000)).content.decode('utf-8')
                                urllib.request.urlretrieve(img_url, filename=path)
                                break
                            except:
                                if tries <(maxTryNum-1):  
                                    continue
                                else:  
                                    logging.error("Has tried %d times to access url %s, all failed!",maxTryNum,img_url)  
                                    break

                    LocalFileSize = Consumer.getLocalFilesize(self, filename = filename)
                    if LocalFileSize != RemoteFileSize:
                        File_Exception_ErrorRaise()

                except File_Exception:
                    print('文件名：', filename)
                    print('目标文件大小：', RemoteFileSize, '   ', '本地文件大小：', )
                    print('(3sec)准备重新下载...')
                    time.sleep(3)
                    print('正在下载新文件...')
                    print('新文件将存储在ErrorFiles文件夹下...')
                    time.sleep(1)

                    error_file_folder = './ErrorFiles'
                    error_file = filename
                    error_path = error_file_folder + '/' + error_file

                    errorlist.append(error_file)
                    os.mkdir(error_file_folder)

                    urllib.request.urlretrieve(img_url, filename=error_path)

                if len(imglist)==0:
                    end=time.time()
                    print("消耗的时间为：", (end - start), "秒")
                    Consumer.stop(self)

    def getRemoteFileSize(self, url, proxy=None):
        """ 
        通过content-length头获取远程文件大小（单位为Bytes）;
        url - 目标文件URL;
        proxy - 代理
        """
        opener = urllib.request.build_opener()
        if proxy:
            if url.lower().startswith('https://'):
                opener.add_handler(urllib.request.ProxyHandler({'https' : proxy}))
            else:
                opener.add_handler(urllib.request.ProxyHandler({'http' : proxy}))
        try:
            request = urllib.request.Request(url)
            request.get_method = lambda: 'HEAD'
            response = opener.open(request)
            response.read()
        except Exception:
            return 0
        else:
            #print(response.headers)
            fileSize = dict(response.headers).get('Content-Length', 0)
            return int(fileSize)
    

    def getLocalFilesize(self, filename):
        """
        获取本地文件大小（单位为Bytes）;
        filename:文件名
        """
        global folder
        imgpath = './' + str(folder) + '/' + filename
        LocalSize = os.path.getsize(imgpath)
        return int(LocalSize)

    def stop(self):
        """
        线程执行完毕后的退出指令
        """
        global errorlist
        BoolValue = threading.Thread.isAlive(self)
        if not BoolValue:
            print('线程运行完成！')
            print('下载不完整的任务数：', len(errorlist), '请自行删除...')
            time.sleep(3)

            keyboard = str(input('按enter键退出...'))
            if keyboard == '':
                exit()
            else:
                print('按键有误！')
                print('5秒后程序自动退出...')
                time.sleep(5)
                exit()






if __name__ == '__main__':
    page_links_list=[str(input("请输入要抓取的网址："))]

    last_page_number_pro = Getlastpage()

    print("（总共",last_page_number_pro,"页）")

    key=str(page_links_list[0])
    key_pro=key[32:]    #字符串切片得到关键词

    GetUrls(page_links_list)

    folder = str(input('请输入要存储的文件夹（直接回车为images）：'))

    if folder == '':
        folder = 'images'

    Folder = './' + folder

    if os.path.exists(Folder):
        print('所要创建的文件夹已存在！')
        print("文件夹将被命名为：'_+Folder'")
        _Folder = '_' + folder
        os.mkdir(_Folder)
    else:
        os.mkdir(Folder)

    start=time.time()
    # 1个生产者线程，去从页面中爬取图片链接
    for x in range(1):
        Producer().start()

    # 10个消费者线程，去从页面中提取下载链接，然后下载
    for x in range(10):
        Consumer().start()
