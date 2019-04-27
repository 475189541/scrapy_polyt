import requests
import json

url = "https://mxhdjy.polyt.cn/doLogin/login"
formdata = {
            'userName': '17758686920',
            'passWord': 'IYw+1j/+pSbcaUT1Kg4zqS2Jsuw=',
            'loginFlag': 'false'
        }
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Cookie': 'acw_tc=76b20f6a15563889356293647e4f41554cf2c2836b9b398f94e4c69f731c68; JSESSIONID=BBE0A0C20BB53B787397C19BE557D1D7; Hm_lvt_ed7069d2834bd9d2dcff979303c93b71=1556388935; Hm_lpvt_ed7069d2834bd9d2dcff979303c93b71=1556388935'}
session = requests.Session()
response = session.post(url=url, data=formdata, headers=headers)
print(response.text)