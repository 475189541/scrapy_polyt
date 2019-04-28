import scrapy
import re
import time
import json
import hashlib
from urllib.parse import urlencode


class SpidersPolytSpider(scrapy.Spider):
    name = 'spiders_polyt'
    allowed_domains = ['mxhdjy.polyt.cn']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_polyt.pipelines.ScrapyPolytPipeline': 300, },
        # 'HTTPERROR_ALLOWED_CODES': [405],
        'COOKIES_ENABLED': True,
        # 'DOWNLOAD_DELAY ': 0.2,
        'LOG_LEVEL': 'WARNING'

        }

    def __init__(self, **kwargs):
        super(SpidersPolytSpider, self).__init__()
        self.pattern_arg1 = re.compile("arg1='([^']+)'")
        self.key = '3000176000856006061501533003690027800375'
        self.base_url = 'https://mxhdjy.polyt.cn/'
        self.cookie_id = 'ed7069d2834bd9d2dcff979303c93b71'
        self.key_work = ['声入人心']
        self.showTime = '2019-05-11,2019-05-11'

    def filter_data(self, d):
        name = d.xpath('./h2/a/text()').extract_first()
        href = d.xpath('./h2/a/@href').extract_first()
        data = {'name': name, 'href': href}
        if name:
            for key_work in self.key_work:
                if key_work in name:
                    return data

    def hash_str(self, data):
        """
        生成hash的方法封装  用于生产固定字符串的hash值
        :param data: 字符串
        :return hash: 字符串hash值
        """
        md5 = hashlib.md5()
        md5.update(str(data).encode())
        return md5.hexdigest()

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
        meta = {'cookiejar': 1, 'Cookie': {}}
        yield scrapy.Request(url=self.base_url, dont_filter=True, callback=self.parse, meta=meta)

    def parse(self, response):
        cookiejar, cookies = response.meta['cookiejar'], response.meta['Cookie']
        hex_xor = self.get_hexXor(response=response)
        SetCookie = response.headers.getlist('Set-Cookie')
        Cookie = map(lambda c: c.decode('utf-8').replace('Path', 'path').split('path')[0], SetCookie)
        cookie = dict(map(lambda x: tuple(x.strip().rstrip(';').split('=')), Cookie))
        cookies.update(cookie)
        if hex_xor:
            if not cookies.get('acw_sc__v2'):
                cookies['acw_sc__v2'] = hex_xor
            else:
                cookies['acw_sc__v3'] = hex_xor
        url = "https://mxhdjy.polyt.cn/doLogin/login"
        formdata = {
            'userName': '17758686920',
            'passWord': 'IYw+1j/+pSbcaUT1Kg4zqS2Jsuw=',
            'loginFlag': 'true'
        }
        meta = {'cookiejar': cookiejar}
        yield scrapy.FormRequest(url=url, callback=self.parse_login, meta=meta, formdata=formdata, cookies=cookies)

    def parse_login(self, response):
        data = json.loads(response.text, encoding='utf-8')
        if data.get('Y'):
            self.logger.warning('登录成功')
            cookiejar = response.meta['cookiejar']
            data = {
                'catalogName': '', 'showPrice': '', 'showTime': self.showTime,
                'timeSort': '', 'queryString': '', 'priceSort': '',
                'theaterId': 760, 'currentPage': 1, 'pageSize': 2
            }
            base_url = 'https://mxhdjy.polyt.cn/toSearchTheatreList?'
            url = base_url + urlencode(data)
            meta = {'cookiejar': cookiejar}
            yield scrapy.Request(url=url, callback=self.parse_search, meta=meta, dont_filter=True)
        else:
            self.logger.warning('登录失败')

    def parse_search(self, response):
        cookiejar = response.meta['cookiejar']
        div_tree = response.xpath('//div[@class="fl card-cont-box"]')
        datas = list(filter(lambda f: f, map(lambda d: self.filter_data(d), div_tree)))
        for data in datas:
            name = data.get('name')
            href = data.get('href')
            url = self.base_url + href
            meta = {'cookiejar': cookiejar}
            self.logger.warning('找到 %s' % name)
            yield scrapy.Request(url=url, callback=self.parse_detal, meta=meta, dont_filter=True)
        if not datas:
            self.logger.error('未能找到 %s' % self.key_work)

    def parse_detal(self, response):
        showId = response.xpath('//input[@id="showId"]/@value').extract_first()
        placeId = response.xpath('//input[@id="placeId"]/@value').extract_first()
        venueId = response.xpath('//input[@id="venueId"]/@value').extract_first()
        projectId = response.xpath('//input[@id="projectId"]/@value').extract_first()
        showTime = response.xpath('//input[@id="showTimeOld"]/@value').extract_first()
        theaterId = response.xpath('//input[@id="theaterId"]/@value').extract_first()
        productId = response.xpath('//input[@id="productId"]/@value').extract_first()
        isRealName = '0'
        ticketNumber = response.xpath('//input[@id="ticketNumber"]/@value').extract_first()
        manageWayCode = response.xpath('//input[@id="manageWayCode"]/@value').extract_first()
        productTypeName = response.xpath('//input[@id="productTypeName"]/@value').extract_first()
        productSubtypeName = response.xpath('//input[@id="productSubtypeName"]/@value').extract_first()
        threaterName = response.xpath('//input[@id="threaterName"]/@value').extract_first()
        purchaseRestrictions = response.xpath('//span[@id="purchaseRestrictions"]/text()').extract_first()
        sign = self.hash_str(theaterId + projectId + showId) + '123'
        cookiejar = response.meta['cookiejar']
        meta = {'cookiejar': cookiejar, 'showId': showId, 'placeId': placeId, 'venueId': venueId,
                'projectId': projectId, 'showTime': showTime, 'theaterId': theaterId, 'productId': productId,
                'isRealName': isRealName, 'ticketNumber': ticketNumber, 'manageWayCode': manageWayCode,
                'productTypeName': productTypeName, 'productSubtypeName': productSubtypeName,
                'threaterName': threaterName, 'purchaseRestrictions': purchaseRestrictions, 'sign': sign}
        url = 'https://mxhdjy.polyt.cn/chooseSeat/openArea'
        formdata = {
            'showId': showId,
        }
        yield scrapy.FormRequest(url=url, callback=self.parse_open_area, meta=meta, formdata=formdata, dont_filter=True)

    def parse_open_area(self, response):
        datas = json.loads(response.text, encoding='utf-8')
        cookiejar = response.meta['cookiejar']
        showId = response.meta['showId']
        placeId = response.meta['placeId']
        venueId = response.meta['venueId']
        projectId = response.meta['projectId']
        showTime = response.meta['showTime']
        theaterId = response.meta['theaterId']
        productId = response.meta['productId']
        isRealName = response.meta['isRealName']
        ticketNumber = response.meta['ticketNumber']
        manageWayCode = response.meta['manageWayCode']
        productTypeName = response.meta['productTypeName']
        productSubtypeName = response.meta['productSubtypeName']
        threaterName = response.meta['threaterName']
        purchaseRestrictions = response.meta['purchaseRestrictions']
        sign = response.meta['sign']
        sectionId = datas['data']['sectionId']
        seat_list = list(filter(lambda f: f, map(lambda x: x if x['sst']['name'] != '已售' else None, datas['data']['seatList'])))
        seat = seat_list[0]
        priceList = list(filter(lambda f: f if f['ticketPriceId'] == seat['pid'] else None, datas['data']['priceList']))
        price_data = {"data": [{
                    "price": priceList[0]['price'],
                    "priceId": seat['pid'],
                    "seat": seat['sid'],
                    "count": "1",
                    "actuallyPrice": priceList[0]['price'],
                    "freeTicketCount": "1"
                  }],
                      "param": {
                  "theaterId": theaterId,
                  "projectId": projectId,
                  "date": int(time.time() * 1000),
                  "showId": showId,
                  "showTime": showTime,
                  "placeId": placeId,
                  "venueId": venueId,
                  "isRealName": isRealName,
                  "sign": sign,
                  "manageWayCode": manageWayCode
                }}
        formdata = {
            "param": json.dumps(price_data, ensure_ascii=False),
            "sign": sign
        }
        url = 'https://mxhdjy.polyt.cn/submitOrderSeat'
        meta = {'cookiejar': cookiejar, 'data': datas['data'], 'showId': showId, 'placeId': placeId, 'venueId': venueId,
                'projectId': projectId, 'showTime': showTime, 'theaterId': theaterId, 'productId': productId,
                'isRealName': isRealName, 'ticketNumber': ticketNumber, 'manageWayCode': manageWayCode,
                'productTypeName': productTypeName, 'productSubtypeName': productSubtypeName,
                'threaterName': threaterName, 'purchaseRestrictions': purchaseRestrictions, 'sign': sign,
                'sectionId': sectionId}
        yield scrapy.FormRequest(url=url, callback=self.parse_view_skip, meta=meta, dont_filter=True, formdata=formdata)

    def parse_view_skip(self, response):
        cookiejar = response.meta['cookiejar']
        data = response.meta['data']
        showId = response.meta['showId']
        placeId = response.meta['placeId']
        venueId = response.meta['venueId']
        projectId = response.meta['projectId']
        showTime = response.meta['showTime']
        theaterId = response.meta['theaterId']
        productId = response.meta['productId']
        isRealName = response.meta['isRealName']
        ticketNumber = response.meta['ticketNumber']
        manageWayCode = response.meta['manageWayCode']
        productTypeName = response.meta['productTypeName']
        productSubtypeName = response.meta['productSubtypeName']
        threaterName = response.meta['threaterName']
        purchaseRestrictions = response.meta['purchaseRestrictions']
        sectionId = response.meta['sectionId']
        html_string = response.text
        formdata = {
            'deliveryWay': re.search('var \$deliveryWay = [\'|\"](.*?)[\'|\"];', html_string).group(1),
            'username': response.xpath('//input[@id="consignee"]/@value').extract_first(),
            'phone': re.search('var \$defaultPhone = [\'|\"](.*?)[\'|\"];', html_string).group(1),
            'deliveryArea': re.findall('\$logisticsScope = [\'|\"](.*?)[\'|\"];', html_string)[1],
            'consigneeId': response.xpath('//input[@id="consigneeId"]/@value').extract_first(),
            'consignee': response.xpath('//input[@id="consignee"]/@value').extract_first(),
            'receivingAddress': response.xpath('//input[@id="receivingAddress"]/@value').extract_first(),
            'consigneePhonr': response.xpath('//input[@id="consigneePhonr"]/@value').extract_first(),
            'payWayCode': response.xpath('//span[@id="weixinPay"]/@data').extract_first(),
            'isRealName': isRealName,
            'accountBalance': re.search('var \$accountBalance = [\'|\"](.*?)[\'|\"];', html_string).group(1),
            'integral': re.search('var \$integral = [\'|\"](.*?)[\'|\"];', html_string).group(1),
            'rankId': re.search('var \$rankId = [\'|\"](.*?)[\'|\"];', html_string).group(1),
            'inintCount': re.search('var \$inintCount = [\'|\"](.*?)[\'|\"];', html_string).group(1),
            'isHasRank': re.search('var \$isHasRank = [\'|\"](.*?)[\'|\"];', html_string).group(1),
            'theaterId': theaterId,
            'projectId': projectId,
            'projectName': re.search('var \$projectName = [\'|\"](.*?)[\'|\"];', html_string).group(1),
            'showId': showId,
            'showTime': showTime,
            'venueId': venueId,
            'placeId': placeId,
            'UUID': response.xpath('//input[@name="UUID"]/@value').extract_first(),
            'orderTotalAmt': re.search('var \$showPrice = [\'|\"](.*?)[\'|\"];', html_string).group(1),
            'discountAmt': re.search('var \$discountPrice = [\'|\"](.*?)[\'|\"];', html_string).group(1),
            'orderFreightAmtId': response.xpath('//input[@class="freight"]/@value').extract_first().split('_')[-1],
            'orderFreightAmt': re.search('orderFreightAmt:"(.*?)"', html_string).group(1),
            'actuallyPaidAmt': re.search('var \$actuallyPrice = [\'|\"](.*?)[\'|\"];', html_string).group(1)
        }
        url = 'https://mxhdjy.polyt.cn/create'
        meta = {'cookiejar': cookiejar, 'data': data, 'showId': showId, 'placeId': placeId, 'venueId': venueId,
                'projectId': projectId, 'showTime': showTime, 'theaterId': theaterId, 'productId': productId,
                'isRealName': isRealName, 'ticketNumber': ticketNumber, 'manageWayCode': manageWayCode,
                'productTypeName': productTypeName, 'productSubtypeName': productSubtypeName,
                'threaterName': threaterName, 'purchaseRestrictions': purchaseRestrictions, 'sectionId': sectionId}
        yield scrapy.FormRequest(url=url, callback=self.parse_create, meta=meta, dont_filter=True, formdata=formdata)

    def parse_create(self, response):
        title = response.xpath('//title/text()').extract_first()
        if title and title.strip() == '订单支付页':
            self.logger.warning('订单创建成功')
        else:
            self.logger.warning('订单创建失败')





