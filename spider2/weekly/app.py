import pymongo
import time
import configparser
from datetime import datetime as dt
import datetime
from collections import defaultdict
import json
import os
from pathlib import Path
import pathlib
import requests
import numpy as np
import pandas as pd
import hmac
import hashlib
import base64
import urllib.parse
import json
import time
import configparser
from datetime import datetime as dt
import datetime
import os
from pathlib import Path
import pathlib
class ProvinceHandler:
    def __init__(self):
        self.equips = set()
        self.yin = 0
        self.yang = 0
        self.wu = 0
    def __str__(self):
        # return  str(self.yin) + "  " + str(self.yang) + "  " + str(self.wu) + '\n' #+ str(len(self.equips))  + '\n' + str(self.equips)
        return str(len(self.equips)) + '|' + str(self.yin) + '|' + str(self.yang) + '|' + str(self.wu) + '|' + str(self.yin+self.yang+self.wu) + '|'


class BatchHandler:
    def __init__(self):
        self.yin = 0
        self.yang = 0
        self.wu = 0
    
    def __str__(self):
        return str(self.yin) + '|' + str(self.yang) + '|' + str(self.wu) + '|' + str(self.wu+self.yang+self.yin) + '|' + '\n'


current_parent_dir = pathlib.Path(__file__).parent.parent.absolute()
CONFIG_FILE_PATH = os.path.join(current_parent_dir, 'conf.ini')
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)
TABLE = config.get('database', 'TABLE')
DB = config.get('database', 'DB')

def yin_yang(item):
    conclusions = []
    conclusions.append(item['conclusion1'])
    conclusions.append(item['conclusion2'])
    conclusions.append(item['conclusion3'])
    if '阳性' in conclusions:
        return '阳'
    if '无效' in conclusions:
        return '无'
    return '阴' 
    
print(TABLE)
print(DB)

client = pymongo.MongoClient('localhost')
db = client[DB]
table = db[TABLE]

now = dt.now()
one_week_ago = now + datetime.timedelta(weeks=-1)
query = {"create_time": {"$gt":one_week_ago, "$lt":now}}
items = table.find(query)

d = defaultdict(ProvinceHandler)
for item in items:
    item = dict(item)
    if item['address'] == '':
        continue
    province = item['address'].split()[0]
    conclusion = yin_yang(item)
    # print(conclusion)
    # d[province][conclusion] += 1
    
    d[province].equips.add(item['SNcode'])

    if conclusion == '阴性':
        d[province].yin += 1
    elif conclusion == '阳性':
        d[province].yang += 1
    else:
        d[province].wu += 1

province_msg = '| 序号 | 省份 | 设备数 | 阴性数 | 阳性数 | 无效数 | 检测总量 |\n | ---- | ---- | ------ | ------ | ------ | ------ | -------- | \n'
total = [0] * 6
for index, key in enumerate(d.keys()) :
    province_msg += '|' + str(index+1) + '|' + str(key) + '|' + str(d[key]) + '\n'
    # print(index, key, d[key], sep='\t')
    total[1] += len(d[key].equips)
    total[2] += d[key].yin
    total[3] += d[key].yang
    total[4] += d[key].wu
total[5] = sum(total[:-1])
province_msg += '| 合计 |/|' + '|'.join([str(i) for i in total]) + '|'

print(province_msg)


now = dt.now()
one_week_ago = now + datetime.timedelta(weeks=-1)
query = {"create_time": {"$gt":one_week_ago, "$lt":now}}
items = table.find(query)

d_batch = defaultdict(BatchHandler)
for item in items:
    item = dict(item)
    if item['sBatchCode'] == '':
        continue
    batch = item['sBatchCode']
    conclusion = yin_yang(item)


    if conclusion == '阴性':
        d_batch[batch].yin += 1
    elif conclusion == '阳性':
        d_batch[batch].yang += 1
    else:
        d_batch[batch].wu += 1

batch_msg = '| 批次号      | 阴性数 | 阳性数 | 无效数 | 检测总量 | \n | ---- | ---- | ------ | ------ | ------ | ------ | -------- |\n' 
total = [0] * 4
for key in d_batch.keys():
    # print(key)
    # print(d_batch[key])
    batch_msg += '|' + str(key) + '|' + str(d_batch[key].yin) + '|' +  str(d_batch[key].yang) + '|' +  str(d_batch[key].wu) + '|' + str( d_batch[key].wu +  d_batch[key].yang + d_batch[key].yin) + '|\n' 
    total[0] += d_batch[key].yin
    total[1] += d_batch[key].yang
    total[2] += d_batch[key].wu
total[3] = sum(total[:-1])
batch_msg += '| 总计   |' + '|'.join([str(i) for i in total]) + '|'
print(batch_msg)


class dingTalk():
    def __init__(self):
        # self.access_token = '5bb414bbd12ccb74196b58cb21893c3a36743889dc78e0ef2a6c5d2888a631d9'
        # self.secret = 'SEC3cf584e906ff16ca465b26e7324eba304a8f18f9e88171c4e6c4afcb7cb96326'
        self.access_token = config.get('dingtalk', 'access_token')
        self.secret = config.get('dingtalk', 'secret')
    def get_params(self):
        timestamp = str(round(time.time() * 1000))
        # secret = 'SEC3cf584e906ff16ca465b26e7324eba304a8f18f9e88171c4e6c4afcb7cb96326'
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign
    def msg(self, markdown_text):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "test",
                "text": markdown_text

            },
            "at": {
                "isAtAll": False
            }
        }
        json_data = json.dumps(data)
        print(json_data)
        timestamp, sign = self.get_params()
        print(timestamp, sign)
        response = requests.post(
            url='https://oapi.dingtalk.com/robot/send?access_token={access_token}&sign={sign}&timestamp={timestamp}'.format(access_token=self.access_token, sign=sign, timestamp=timestamp), data=json_data, headers=headers)
        return response
dingtalk = dingTalk()
response = dingtalk.msg(province_msg+'\n\n\n'+batch_msg)

print(response.text)