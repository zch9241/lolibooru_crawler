import urllib.request


def getRemoteFileSize(url, proxy=None):
    """ 
    通过content-length头获取远程文件大小（单位为Bytes）;
    url - 目标文件URL;
    proxy - 代理
    """
    print('1')
    opener = urllib.request.build_opener()
    print('2')
    if proxy:
        if url.lower().startswith('https://'):
                opener.add_handler(urllib.request.ProxyHandler({'https' : proxy}))
        else:
                opener.add_handler(urllib.request.ProxyHandler({'http' : proxy}))
    try:
        print('3')
        request = urllib.request.Request(url)
        print('4')
        request.get_method = lambda: 'HEAD'
        print('5')
        response = opener.open(request)
        print('6')
        response.read()
        print('7')
    except Exception:
        return 0
    else:
        print('8')
        print(response.headers)
        fileSize = dict(response.headers).get('Content-Length', 0)
        return int(fileSize)

url = 'https://lolibooru.moe/image/215e18b147d04f7db618b8796b60982a/lolibooru%20356212%20elbow_gloves%20final_fantasy%20final_fantasy_vii%20fingerless_gloves%20katori_(mocchidou)%20large_breasts%20looking_at_viewer%20suspender_skirt%20tifa_lockhart.png'

test = getRemoteFileSize(url = url)
print(test)
