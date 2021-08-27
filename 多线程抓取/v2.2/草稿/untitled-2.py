from bs4 import BeautifulSoup
import os
import re
import requests
import threading
import time
import urllib.request
import urllib.parse

import response

def getRemoteFileSize(url, proxy=None):
    """ 通过content-length头获取远程文件大小
        url - 目标文件URL
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
        print(response.headers)
        fileSize = dict(response.headers).get('Content-Length', 0)
        return int(fileSize)

url = 'https://lolibooru.moe/image/63646989e495506a3dbbd33fa8140668/lolibooru%20356089%20cardcaptor_sakura%20looking_at_viewer%20own_hands_together%20simple_background%20tomoeda_elementary_school_uniform%20white_background%20white_sailor_collar.png'

size = getRemoteFileSize(url = url)

print(size)

def get():
    global url
    path = 'test'
    urllib.request.urlretrieve(url, filename=path)

#def size(a,b,c):

#    print(c)


get()


#requests.get().headers['Content-Length']



#response = requests.get()
 
#expected_length = response.headers.get('Content-Length')
#if expected_length is not None:
#    actual_length = response.raw.tell()
#    expected_length = int(expected_length)
#    if actual_length < expected_length:
#        raise IOError(
#            'incomplete read ({} bytes read, {} more expected)'.format(
#                actual_length,
#                expected_length - actual_length
#            )
#        )