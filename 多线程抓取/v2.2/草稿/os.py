import os
import urllib.request
# 获取本地文件大小
size = os.path.getsize('test.txt')

print(size)


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