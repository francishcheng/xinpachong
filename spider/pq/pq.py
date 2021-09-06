import warnings
import pymongo
import os
import datetime 
from datetime import datetime as dt
from collections import defaultdict
import configparser
import time, hmac, urllib, base64, hashlib, json, requests
import pathlib
from collections import defaultdict
current_parent_dir = pathlib.Path(__file__).parent.parent.absolute()
CONFIG_FILE_PATH = os.path.join(current_parent_dir, 'conf.ini')
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)
def num(float_n):
    return float_n.split('.')[0] + '.' +float_n.split('.')[1][:2]

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
class X():
    def __init__(self, id, total_num, warning_num, serial, location) -> None:
        self.id = id
        self.total_num = total_num
        self.warning_num = warning_num
        self.serial = serial
        self.localtion = location
        self.rate = self.warning_num / self.total_num

class Cal():

    def __init__(self, types):
        self.types = types
        self.warning_num = defaultdict(int)
        self.total_num = defaultdict(int)
        self.localtion = defaultdict(str)
        self.serial = defaultdict(str)
        self.ids = set()
        self.l = None
    def add(self, item):
        if self.types == 'p':
            id= item.get('sBatchCode') + '/' +item.get('ItemID')
        else:
            id = item['SNcode']
        self.ids.add(id)
        self.localtion[id] = item['address']
        self.serial[id] = item['SNcode']
        self.total_num[id] += 1
        if item.get('warning') != 0:
            self.warning_num[id] += 1 
    def calculate(self):
        if self.l is not None:
            return
        l = []
        for id in self.ids:
            # print(id)
            # print(self.total_num[id])
            # print(self.warning_num[id])
            # print(self.serial[id])
            # print(self.localtion[id])
            # print('-'*10)
            l.append(X(id, self.total_num[id], self.warning_num[id], self.serial[id], self.localtion[id]))
        self.l = l
def res_7days(table):
    now = dt.now()
    query = {}		
    # one_week_ago = now + datetime.timedelta(weeks=-1)
    today = dt(now.year, now.month, now.day)
    res = []
    for i in range(7):
        start = today + datetime.timedelta(days=(-i+1))
        end = start + datetime.timedelta(days=-1)
        # print(start)
        # print(end)
        # print('-' * 10)
        query = {"create_time": {"$gt":end, "$lt":start}}
        items = table.find(query)
        res.append(items)
    return res
def today(table):
    now = dt.now()
    query = {}  
    yesterday = now + datetime.timedelta(days=-1)
    query = {"create_time": {"$gt": yesterday, "$lt": now}}
    items = table.find(query)
    return items
def report():
    TOP_N = 5
    dingtalk = dingTalk()
    # values = [120, 200, 150, 80, 70, 110, 130]
    current_parent_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
    print(current_parent_dir)
    CONFIG_FILE_PATH = os.path.join(current_parent_dir, 'conf.ini')
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    TABLE = config.get('database', 'TABLE')
    DB = config.get('database', 'DB')
    client = pymongo.MongoClient('localhost')
    db = client[DB]
    table = db[TABLE]

    msg = ''
    msg += dt.now().strftime("%Y-%m-%d %H:%M") + '\n\n'
    msg += '批次号   项目号     报警次数    报警比例（P）   \n\n '
    items = today(table)
    p_cal = Cal('p')
    for item in items:
        # print(dict(item))
        p_cal.add(item)
    p_cal.calculate()
    p_cal.l = sorted(p_cal.l,  key=lambda x: x.rate, reverse=True)
    for item in p_cal.l[:TOP_N+1]:
        # print(item.id.split('/')[0],item.id.split('/')[1] ,item.total_num, item.rate)
        msg += '-' * 10  + '\n\n'
        msg += str(item.id.split('/')[0])+ '\n\n' + str(item.id.split('/')[1]) + '\n\n' +  str(item.total_num) +'\n\n' + num(str(item.rate))
        msg += '\n\n'
        msg += '-' * 10 + '\n\n'
    print(msg)
    response = dingtalk.msg(msg)
    print(response.status_code)
    msg = ''
    msg += dt.now().strftime("%Y-%m-%d %H:%M") + '\n\n'
    msg += '地区     序列号     报警次数   报警比例（Q）   \n\n'
    items = today(table)
    print('-' * 10)
    q_cal = Cal('q')
    for item in items:
        q_cal.add(item)
    q_cal.calculate()
    q_cal.l = sorted(q_cal.l, key=lambda x: x.rate, reverse=True)

    for item in q_cal.l[:TOP_N+1]:
        # print(item.localtion, item.serial, item.total_num, item.rate)
        msg += '-'*10 + '\n\n'
        msg += item.localtion+ '\n\n' + item.serial +'\n\n' + str(item.total_num) + '\n\n'+ num(str(item.rate))
        msg += '\n\n'
        msg += '-'*10 + '\n\n'
    print(msg)
    response = dingtalk.msg(msg)
    print(response.status_code)

import schedule
import time

schedule.every().day.at("09:00").do(report)
while True:
    schedule.run_pending()
    time.sleep(1)