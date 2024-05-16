import requests
url = 'http://mercury.picoctf.net:1270'
pm = {'User-Agent' : 'PicoBrowser', 'Referer':'http://mercury.picoctf.net:1270','Date':'2018','DNT':'1','X-Forwarded-For':'104.107.224.0', 'Accept-Language':'sv'}
req = requests.get(url, headers=pm)
print(req.text)