import scrapy
import json
from datetime import datetime
from ..settings import DB, TABLE
import pymongo
import time
import re
from ..items import PachongItem
from ..settings import MAX_PAGE 
import os
import configparser
import pathlib
post_img_url = 'http://58.87.111.39:5555/items/'

class SpiderSpider(scrapy.Spider):
    current_parent_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
    CONFIG_FILE_PATH = os.path.join(current_parent_dir, 'conf.ini')
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    
    name = 'spider'
    domain = config.get('spider', 'domain')
    vendor = config.get('spider', 'vendor')

    # start_urls = ['https://www.helmenyun.cn/index.php/DataManage/data_list/{page}']
    # data_list_url = 'https://www.helmenyun.cn/index.php/DataManage/data_list/{page}'
    # detail_url = 'https://www.helmenyun.cn/index.php/DataManage/data_detail?sql={vendor}&SNcode={SNcode}&sTime={sTime}&RecordID={RecordID}'

    start_urls = [domain + '/index.php/DataManage/data_list/{page}']
    data_list_url =domain + '/index.php/DataManage/data_list/{page}'
    detail_url = domain + '/index.php/DataManage/data_detail?sql={vendor}&SNcode={SNcode}&sTime={sTime}&RecordID={RecordID}'

    client = pymongo.MongoClient('localhost')
    db = client[DB]
    table = db[TABLE]
    def start_requests(self):
        
        for url in self.start_urls:
            yield scrapy.Request(url=url.format(page=1), callback=self.parse)

    def parse(self, response):
        # print(response.body)
        print(response.url)
        page = int(response.url.split('/')[-1])
        trs = response.xpath('//tbody[@class="TbodyList"]//tr')
        # RecordIDs , ItemIDs , BatchIDs , sSampleIDs , sItemNames , sBatchCodes , sTimes , Concentrations , Judges, CValues , TValues =  ([] for i in range(11)) 
        # res = []
        for tr in trs:
            item = PachongItem() 
            item['RecordID'] = tr.xpath('./td[@class="RecordID"]/text()').get(default='') 
            item['ItemID'] = tr.xpath('./td[@class="ItemID"]/text()').get(default='') 
            item['BatchID'] = tr.xpath('./td[@class="BatchID"]/text()').get(default='') 
            item['sSampleID'] = tr.xpath('./td[@class="sSampleID"]/text()').get(default='') 
            item['sItemName'] = tr.xpath('./td[@class="sItemName"]/text()').get(default='')
            item['sBatchCode'] = tr.xpath('./td[@class="sBatchCode"]/text()').get(default='')
            item['sTime'] = tr.xpath('./td[@class="sTime"]/text()').get(default='')
            item['Concentration'] = tr.xpath('./td[@class="Concentration"]/text()').get(default='')
            item['Judge'] = tr.xpath('./td[@class="Judge"]/text()').get(default='') 
            # item['CValue'] = tr.xpath('./td[@class="CValue"]/text()').get(default='') 
            # item['TValue'] = tr.xpath('./td[@class="TValue"]/text()').get(default='')
            item['SNcode'] = tr.xpath('./td[@class="check-bight"]/input/@value').get(default='')   
            item['sTimeNumber'] = tr.xpath('./td[@class="sTime"]/input/@value').get(default='')
            # item['serial_number'] = tr.xpath('')
            # res.append(item)
            
            query = {
               'RecordID' : item['RecordID'] 
            }
            res = self.table.find_one(query)
            if res is None:
                yield scrapy.Request(self.detail_url.format(vendor=self.vendor, SNcode=item['SNcode'], sTime=item['sTimeNumber'], RecordID=item['RecordID']), callback=self.parse_detail, meta={'item':item}, dont_filter=True)    
        # print('RecordIDs', RecordIDs)
        # print('ItemIDs', ItemIDs)
        # print('BatchIDs', BatchIDs)
        # print('sSampleIDs', sSampleIDs)
        # print('sItemNames', sItemNames)
        # print('sBatchCodes', sBatchCodes)
        # print('sTimes', sTimes)
        # print('Concentrations', Concentrations)
        # print('Judges', Judges)
        # print('CValues', CValues)
        # print('TValues', TValues)
        # for ele in res:
        #     print(ele)
        # print(self.data_list_url.format(page=page))
        if page<=MAX_PAGE:
            yield scrapy.Request(self.data_list_url.format(page=page+1), callback=self.parse, dont_filter=True) 
        else:
            print('sleep 6 min')
            time.sleep(6*60)
            yield scrapy.Request(self.data_list_url.format(page=1), callback=self.parse, dont_filter=True) 
        
    def parse_detail(self, response):
        # print(response.url)
        # print(response.meta['item'])
        item = response.meta['item']

        script = response.xpath('//script')[-1].extract()
        pattern = re.compile('curvePoint="(.*?)"') 
        res = re.search(pattern, script)
        points = res.groups(0)[0]
        item['points'] = points        
        item['address'] = response.xpath('//span[@class="address"]/text()').get(default='')   
        # item['data_bight']  = response.xpath('//div[@class="data-bight"]/p').get(default='')
        item['create_time'] = datetime.now()
        item['gender'] = response.xpath('/html/body/div/div/div[1]/div[3]/span[2]/text()').get(default='')
        item['place'] = response.xpath('/html/body/div/div/div[3]/div[1]/span[2]/text()').get(default='')
        data_header = response.xpath("//div[@class='data-header']")[0]
        cons1 = data_header.xpath('//div[@class="row" and position()=4]//div[position()=2]//span[position()=2]/text()').get(default='')
        cons2 = data_header.xpath('//div[@class="row" and position()=5]//div[position()=2]//span[position()=2]/text()').get(default='')
        cons3 = data_header.xpath('//div[@class="row" and position()=6]//div[position()=2]//span[position()=2]/text()').get(default='')
        conclusion1 = data_header.xpath('//div[@class="row" and position()=4]//div[position()=4]//span[position()=2]/text()').get(default='')
        conclusion2 = data_header.xpath('//div[@class="row" and position()=5]//div[position()=4]//span[position()=2]/text()').get(default='')
        conclusion3 = data_header.xpath('//div[@class="row" and position()=6]//div[position()=4]//span[position()=2]/text()').get(default='')
        item['cons1'] = cons1
        item['cons2'] = cons2
        item['cons3'] = cons3
        item['conclusion1'] = conclusion1
        item['conclusion2'] = conclusion2
        item['conclusion3'] = conclusion3
        data_bight  = response.xpath('//div[@class="data-bight"]/p')
        CValue = data_bight.xpath('//span[@class="CValue"]/text()').get(default='')
        TValue1 = data_bight.xpath('//span[@class="TValue" and position()=4]/text()').get(default='')
        TValue1 = TValue1.strip()
        TValue2 = data_bight.xpath('//span[@class="TValue" and position()=6]/text()').get(default='')
        TValue3 = data_bight.xpath('//span[@class="TValue" and position()=8]/text()').get(default='')
        item['CValue']  = CValue
        item['TValue1'] = TValue1
        item['TValue2'] = TValue2
        item['TValue3'] = TValue3
        
        # print(item)
        yield item
        # data = {
        #     "points":item["points"], 
        #     "TABLE":  TABLE,
        #     "RecordID": item["RecordID"]
        # }
        # json_data = json.dumps(data)
        # # response = requests.post(post_img_url, data=json_data)
        # # if response.status_code != 200:
        # #     print("cannot upload img"+ str(item['RecordID'])) 
        # yield scrapy.Request(post_img_url, method='POST', body=json_data)

        
