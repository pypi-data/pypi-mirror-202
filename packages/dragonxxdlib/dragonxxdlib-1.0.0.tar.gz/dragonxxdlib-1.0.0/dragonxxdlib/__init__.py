import requests
def youtube(urly):
    url="https://api.onlinevideoconverter.pro/api/convert"
    data='{"url":"%s"}' %(urly)
    head={
'Host': 'api.onlinevideoconverter.pro',
'accept': 'application/json, text/plain, */*',
'content-type': 'application/json',
'user-agent': 'Mozilla/5.0 (Linux; Android 9; CPH2083) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
'origin': 'https://en.onlinevideoconverter.pro',
'referer': 'https://en.onlinevideoconverter.pro/',
'content-length': '' + str(len(data)) + '',
    }
    r=requests.post(url,headers=head,data=data).json()
    json=r['url'][0]['url']
    return json


def tiktok(urlt):
    url2="https://api.onlinevideoconverter.pro/api/convert"
    data2='{"url":"%s"}' %(urlt)
    head2={
'Host': 'api.onlinevideoconverter.pro',
'accept': 'application/json, text/plain, */*',
'content-type': 'application/json',
'user-agent': 'Mozilla/5.0 (Linux; Android 9; CPH2083) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
'origin': 'https://en.onlinevideoconverter.pro',
'referer': 'https://en.onlinevideoconverter.pro/',
'content-length': '' + str(len(data2)) + '',
    }
    r2=requests.post(url2,headers=head2,data=data2).json()
    json2=r2['url'][0]['url']
    return json2

def facebook(urlf):
    url2="https://api.onlinevideoconverter.pro/api/convert"
    data2='{"url":"%s"}' %(urlf)
    head2={
'Host': 'api.onlinevideoconverter.pro',
'accept': 'application/json, text/plain, */*',
'content-type': 'application/json',
'user-agent': 'Mozilla/5.0 (Linux; Android 9; CPH2083) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
'origin': 'https://en.onlinevideoconverter.pro',
'referer': 'https://en.onlinevideoconverter.pro/',
'content-length': '' + str(len(data2)) + '',
    }
    r2=requests.post(url2,headers=head2,data=data2).json()
    json2=r2['url'][0]['url']
    return json2

