# from Judge import judge_func
import numpy as np
import pandas as pd
import pymongo
import requests
import hmac
import hashlib
import base64
import urllib.parse
import json
import time
import configparser
from datetime import datetime as dt
from Judge import judge_youxiao
import datetime
import os
from pathlib import Path
import pathlib
current_parent_dir = pathlib.Path(__file__).parent.parent.absolute()
CONFIG_FILE_PATH = os.path.join(current_parent_dir, 'conf.ini')
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)
TABLE = config.get('database', 'TABLE')
DB = config.get('database', 'DB')

print(TABLE)
print(DB)
client = pymongo.MongoClient('localhost')
db = client[DB]
table = db[TABLE]
previous_RecordID = []

class dingTalk():
    def __init__(self):
        # self.access_token = '5bb414bbd12ccb74196b58cb21893c3a36743889dc78e0ef2a6c5d2888a631d9'
        # self.secret = 'SEC3cf584e906ff16ca465b26e7324eba304a8f18f9e88171c4e6c4afcb7cb96326'
        self.access_token = config.get('dingtalk', 'access_token')
        self.secret = config.get('dingtalk', 'secret')
        print(self.access_token)
        print(self.secret)
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
        # print(json_data)
        timestamp, sign = self.get_params()
        print(timestamp, sign)
        response = requests.post(
            url='https://oapi.dingtalk.com/robot/send?access_token={access_token}&sign={sign}&timestamp={timestamp}'.format(access_token=self.access_token, sign=sign, timestamp=timestamp), data=json_data, headers=headers)
        return response
dingtalk = dingTalk()
def has_problem(item):
    if item['conclusion1'].strip() !='阴性' and item['conclusion1'].strip() != '':
        print(item['conclusion1'])
        return True
    if item['conclusion2'].strip() !='阴性' and item['conclusion2'].strip() != '':
        print(item['conclusion2'])
        return True
    if item['conclusion3'].strip() !='阴性' and item['conclusion3'].strip() != '':
        print(item['conclusion3'])
        return True
    return False
COUNT = 0
while True:
    l = []
    msg = ''
    now = dt.now()
    five_mins_ago = now + datetime.timedelta(minutes=-6)
    query = {"create_time": {"$gt":five_mins_ago, "$lt":now}}
    items = table.find(query)
    if COUNT %9==0:
        dingtalk.msg(str(dt.now()))
    COUNT += 1     
    for item in items:
        # print(item)
        item = dict(item)
        if item['RecordID'] not in previous_RecordID and int(item['judge_res'])==0 or has_problem(item):
            l.append(item['RecordID']) 
            values = []
            for key in item.keys():
                if key!='points' and  key!='create_time' and key!='judge_res':
                    values.append(item[key])
            # print(values)        
    
            msg += '\n\n\n---------------------------------------------\n\n\n'
            msg += '\n序列号:  ' + item["SNcode"] +'\n'
            msg += '\n time:  ' + str(item["create_time"])+ '\n'

            msg += '\n 项目名称:  '+ item["sItemName"]+'\n'
            msg += '\n 序号:  ' + item["RecordID"]+'\n'
            msg += '\n检测结果: ' + item.get('conclusion1') if item.get('conclusion1') else '' 
            msg += item.get('conclusion2') if item.get('conclusion2') else ''
            msg += item.get('conclusion3') if item.get('conclusion3') else '' + '\n\n'
            msg += '\n\n 扫描曲线:\n'
            msg +=  '\n'  + ("C值: " + item.get('CValue') + ' ') if item.get("CValue") else ' '
            msg +=     ("T1值: " + item.get('TValue1')) if item.get("TValue1") +'  ' else '   '
            msg +=     ("T2值: " + item.get('TValue2')) if item.get("TValue2") +'  ' else '   '
            msg +=     ("T1值: " + item.get('TValue1')) if item.get("TValue3") +'  ' else '   '
            msg += '\n\n 批次名称\n' + item.get('sBatchCode') + '\n\n'
            shiji = item.get('sItemName').split('/') 
            
            cons = []
            cons.append(item.get('cons1') if item.get('cons1') else '')
            cons.append(item.get('cons2') if item.get('cons2') else '')
            cons.append(item.get('cons3') if item.get('cons3') else '')
            for i in range(len(shiji)):
                msg += shiji[i] + ': ' + cons[i] + '\n\n'

            # msg += '浓度' + item.get('')  
            msg += '\n 详细地址'+ item.get('address')   + '\n'
            msg += '\n \n'
            msg += '\n \n'
            msg += '\n \n'
            msg += '\n\n![screenshot](http://58.87.111.39/img/{TABLE}_{RecordID}.png)\n\n\n'.format(TABLE=TABLE, RecordID=item['RecordID'])
            msg += '\n\n\n---------------------------------------------\n\n\n'
            warning = ''
            if int(item['warning']) == 1:
                warning = '一级报警'
            elif int(item['warning']) == 2:
                warning = '二级报警'
            elif int(item['warning'])==3:
                warning = '三级报警'
            msg += ' \n\n '+ warning  + '\n\n\n' 
            # judge      
            # judge_res = '无效, 请重新测试' if int(item['judge_res']) == 0 else '有效'
            itemID = 0
            if item['ItemID'] != '':
                itemID = int(item['ItemID'])
            true, reason, reason_s, explain = judge_youxiao(item['points'], int(item['CValue']), itemID )
            
            msg += '判断结果:' +  '有效' if int(item['judge_res'])==1 else '无效' 
            if int(true) == 0:
                msg += '失效原因: ' + reason_s 
    response = dingtalk.msg(msg)
    print(response.status_code)
    time.sleep(5 * 60)
    print("sleep 5  mins")
    
     
