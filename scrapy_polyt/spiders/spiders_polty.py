import scrapy
import re
import time
import json


class SpidersPolytSpider(scrapy.Spider):
    name = 'spiders_polyt'
    allowed_domains = ['mxhdjy.polyt.cn']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_polyt.pipelines.ScrapyPolytPipeline': 300, },
        'HTTPERROR_ALLOWED_CODES': [405],
        'COOKIES_ENABLED': True,
        'DOWNLOAD_DELAY ': 0.2,
        'LOG_LEVEL': 'DEBUG'

        }

    def __init__(self, **kwargs):
        super(SpidersPolytSpider, self).__init__()
        self.pattern_arg1 = re.compile("arg1='([^']+)'")
        self.key = '3000176000856006061501533003690027800375'
        self.base_url = 'https://mxhdjy.polyt.cn/'
        self.cookie_id = 'ed7069d2834bd9d2dcff979303c93b71'

    @staticmethod
    def unsbox(arg):
        _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19,
                     0xd,
                     0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c,
                     0x22, 0x25, 0xc, 0x24]
        _0x4da0dc = [''] * 40
        _0x12605e = ''
        for _0x20a7bf in range(0, len(arg)):
            _0x385ee3 = arg[_0x20a7bf]
            for _0x217721 in range(0, len(_0x4b082b)):
                if _0x4b082b[_0x217721] == _0x20a7bf + 0x1:
                    _0x4da0dc[_0x217721] = _0x385ee3
        _0x12605e = ''.join(_0x4da0dc)
        return _0x12605e

    @staticmethod
    def hexXor(_0x4e08d8, _0x23a392):
        _0x5a5d3b = ''
        _0xe89588 = 0x0
        while _0xe89588 < len(_0x23a392) and _0xe89588 < len(_0x4e08d8):
            _0x401af1 = int(_0x23a392[_0xe89588: _0xe89588 + 0x2], 16)
            _0x105f59 = int(_0x4e08d8[_0xe89588: _0xe89588 + 0x2], 16)
            _0x189e2c = hex(_0x401af1 ^ _0x105f59)
            if len(_0x189e2c) == 0x1:
                _0x189e2c = '\x30' + _0x189e2c
            _0x5a5d3b += _0x189e2c[2:]

            _0xe89588 += 0x2
        return _0x5a5d3b

    def get_hexXor(self, response):
        arg1 = self.pattern_arg1.search(response.text)
        if arg1:
            _0x23a392 = self.unsbox(arg=arg1.group(1))
            hex_xor = self.hexXor(self.key, _0x23a392)
            return hex_xor

    def start_requests(self):
        meta = {'cookiejar': 1}
        yield scrapy.Request(url=self.base_url, dont_filter=True, callback=self.parse, meta=meta)

    def parse(self, response):
        cookiejar = response.meta['cookiejar']
        hex_xor = self.get_hexXor(response=response)
        SetCookie = response.headers.getlist('Set-Cookie')
        Cookie = map(lambda c: c.decode('utf-8').replace('Path', 'path').split('path')[0], SetCookie)
        cookies = dict(map(lambda x: tuple(x.strip().rstrip(';').split('=')), Cookie))
        cookies['Hm_lvt_%s' % self.cookie_id] = int(time.time())
        cookies['Hm_lpvt_%s' % self.cookie_id] = int(time.time())
        if hex_xor:
            cookies['acw_sc__v2'] = hex_xor
        meta = {'Cookie': cookies, 'cookiejar': cookiejar}
        url = 'https://mxhdjy.polyt.cn/doLogin/login'
        formdata = {
            'userName': '17758686920',
            'passWord': 'IYw+1j/+pSbcaUT1Kg4zqS2Jsuw=',
            'loginFlag': 'false'
        }
        yield scrapy.FormRequest(url=url, callback=self.parse_login, meta=meta, cookies=cookies, formdata=formdata)

    def parse_login(self, response):
        cookiejar, cookies = response.meta['cookiejar'], response.meta['Cookie']
        meta = {'Cookie': cookies, 'cookiejar': cookiejar}
        url = 'https://mxhdjy.polyt.cn/doLogin/getLoginUser'
        yield scrapy.FormRequest(url=url, callback=self.parse_is_login, meta=meta, cookies=cookies, method='POST')

    def parse_is_login(self, response):
        cookiejar, cookies = response.meta['cookiejar'], response.meta['Cookie']
        Cookie = response.request.headers.getlist('Cookie')
        print(Cookie)
        print()






