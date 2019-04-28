import requests
import json

url = "https://mxhdjy.polyt.cn/doLogin/login"
# url = 'https://mxhdjy.polyt.cn/doLogin/getLoginUser'
formdata = {
            'userName': '17758686920',
            'passWord': 'IYw+1j/+pSbcaUT1Kg4zqS2Jsuw=',
            'loginFlag': 'false'
        }
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://mxhdjy.polyt.cn/userCenter/index',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept-Encoding': 'gzip,deflate',
    'Cookie': 'acw_tc=76b20f6315564157630761666e0e65d312474ea032d53cc3c1773b87e8299a; JSESSIONID=5576C7B020BF97770077072D0BC41859; acw_tc=76b20f6315564157630761666e0e65d312474ea032d53cc3c1773b87e8299a'
}
session = requests.Session()
response = session.post(url=url, data=formdata, headers=headers)
# response = session.post(url=url, headers=headers)
print(response.text)