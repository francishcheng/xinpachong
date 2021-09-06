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
def res_7days():
	now = dt.now()
	query = {}		
	# one_week_ago = now + datetime.timedelta(weeks=-1)
	today = dt(now.year, now.month, now.day)
	res = []
	for i in range(7):

		start = today + datetime.timedelta(days=(-i+1))
		end = start + datetime.timedelta(days=-1)
		print(start)
		print(end)
		print('-' * 10)
		query = {"create_time": {"$gt":end, "$lt":start}}
		items = table.find(query)
		res.append(len(list(items)))
		# for item in items:
		# 	print(dict(item))
		# res.append(len(items))	
	return res
def res_7weeks():
	now = dt.now()
	query = {}		
	today = dt(now.year, now.month, now.day)
	res = []
	for i in range(7):
		start = today + datetime.timedelta(weeks=(-i+1))
		end = start + datetime.timedelta(weeks=-1)
		print(start)
		print(end)
		print('-' * 10)
		query = {"create_time": {"$gt":end, "$lt":start}}
		items = table.find(query)
		res.append(len(list(items)))
		# for item in items:
		# 	print(dict(item))
		# res.append(len(items))	
	return res
def res_7months():
	now = dt.now()
	query = {}		
	today = dt(now.year, now.month, now.day)
	res = []
	for i in range(7):
		start = today + datetime.timedelta(months=(-i+1))
		end = start + datetime.timedelta(months=-1)
		print(start)
		print(end)
		print('-' * 10)
		query = {"create_time": {"$gt":end, "$lt":start}}
		items = table.find(query)
		res.append(len(list(items)))
		# for item in items:
		# 	print(dict(item))
		# res.append(len(items))	
	return res
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

res = res_7weeks()
print(res)