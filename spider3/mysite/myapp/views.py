from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import os
import datetime 
from datetime import datetime as dt
from collections import defaultdict
import configparser
import pathlib
# Create your views here.
def res_7days(table):
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
def res_7weeks(table):
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
def res_7months(table):
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
def download_view(request):
    current_parent_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
    CONFIG_FILE_PATH = os.path.join(current_parent_dir, 'conf.ini')
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    TABLE = config.get('database', 'TABLE')
    DB = config.get('database', 'DB')

    client = pymongo.MongoClient('localhost')
    db = client[DB]
    table = db[TABLE]
    collections = table.find({})
    with open('test.csv','w', encoding='utf-8') as f:
        f.write('序号,仪器序列号,项目号,批次号,样品编号,项目名称,批次名称,测试时间,浓度1,结论1,C值,T1值,浓度2,浓度3,结论2,结论3,T2值,T3值,省市编号,详细地址\n')
        for collection in collections:
            RecordID = collection['RecordID'] 
            ItemID  = collection['ItemID'] 
            ItemName = collection['sItemName']
            BatchID = collection['BatchID']
            sSampleID= collection['sSampleID']
            sItemName= collection['sItemName']
            sBatchCode= collection['sBatchCode']
            sTime= collection['sTime']
            Concentration  = collection['Concentration']
            Judge= collection['Judge']
            CValue= collection['CValue']
            TValue1 = collection['TValue1']
            TValue2 = collection['TValue2']
            TValue3 = collection['TValue3']
            cons1 = collection['cons1']
            cons2 = collection['cons2']
            cons3 = collection['cons3']
            
            conclusion1 = collection['conclusion1']    
            conclusion2 = collection['conclusion2']    
            conclusion3 = collection['conclusion3']    
            SNcode = collection['SNcode']
            sTimeNumber = collection['sTimeNumber']
            points = collection['points']
            address = collection['address']
            create_time = collection['create_time']
            gender = collection['gender']
            place = collection['place']
            collection = dict(collection)
            l = [RecordID, SNcode, ItemID ,BatchID ,sSampleID ,ItemName ,sBatchCode ,sTimeNumber ,cons1 ,conclusion1 ,CValue ,TValue1 ,cons2 ,cons3 ,conclusion2 ,conclusion3 ,TValue2 ,TValue3 ,'',address]
            for ele in l:
                    f.write(str(ele))   
                    f.write(',')
            f.write('\n')
        collections = table.find({})
        f.write('序号,点1,点2,点3,点4,点5,点6,点7,点8,点9,点10,点11,点12,点13,点14,点15,点16,点17,点18,点19,点20,点21,点22,点23,点24,点25,点26,点27,点28,点29,点30,点31,点32,点33,点34,点35,点36,点37,点38,点39,点40,点41,点42,点43,点44,点45,点46,点47,点48,点49,点50,点51,点52,点53,点54,点55,点56,点57,点58,点59,点60,点61,点62,点63,点64,点65,点66,点67,点68,点69,点70,点71,点72,点73,点74,点75,点76,点77,点78,点79,点80,点81,点82,点83,点84,点85,点86,点87,点88,点89,点90,点91,点92,点93,点94,点95,点96,点97,点98,点99,点100,点101,点102,点103,点104,点105,点106,点107,点108,点109,点110,点111,点112,点113,点114,点115,点116,点117,点118,点119,点120,点121,点122,点123,点124,点125,点126,点127,点128,点129,点130,点131,点132,点133,点134,点135,点136,点137,点138,点139,点140,点141,点142,点143,点144,点145,点146,点147,点148,点149,点150,点151,点152,点153,点154,点155,点156,点157,点158,点159,点160,点161,点162,点163,点164,点165,点166,点167,点168,点169,点170,点171,点172,点173,点174,点175,点176,点177,点178,点179,点180,点181,点182,点183,点184,点185,点186,点187,点188,点189,点190,点191,点192,点193,点194,点195,点196,点197,点198,点199,点200,点201,点202,点203,点204,点205,点206,点207,点208,点209,点210,点211,点212,点213,点214,点215,点216,点217,点218,点219,点220,点221,点222,点223,点224,点225,点226,点227,点228,点229,点230,点231,点232,点233,点234,点235,点236,点237,点238,点239,点240,点241,点242,点243,点244,点245,点246,点247,点248,点249,点250,点251,点252,点253,点254,点255,点256,点257,点258,点259,点260,点261,点262,点263,点264,点265,点266,点267,点268,点269,点270,点271,点272,点273,点274,点275,点276,点277,点278,点279,点280,点281,点282,点283,点284,点285,点286,点287,点288,点289,点290,点291,点292,点293,点294,点295,点296,点297,点298,点299,点300,点301,点302,点303,点304,点305,点306,点307,点308,点309,点310,点311,点312,点313,点314,点315,点316,点317,点318,点319,点320,点321,点322,点323,点324,点325,点326,点327,点328,点329,点330,点331,点332,点333,点334,点335,点336,点337,点338,点339,点340,点341,点342,点343,点344,点345,点346,点347,点348,点349,点350\n')

        for collection in collections:
            f.write(collection['RecordID'])
            f.write(',')
            f.write(collection['points'])
            f.write('\n')
            
    file = open('test.csv', 'r', encoding='utf-8')
    response = HttpResponse(file)
    file.close()
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="data.csv"'
    return response
def index_view(request):
    return HttpResponse('<a href="/download" > <button>下载</button></a>')

def week_view(request, collection_name):
    current_parent_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
    CONFIG_FILE_PATH = os.path.join(current_parent_dir, 'conf.ini')
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    TABLE = config.get('database', 'TABLE')
    client = pymongo.MongoClient('localhost')
    DB = config.get('database', 'DB')
    db = client[DB]
    collections = db.list_collection_names()
    collection_name = collection_name if collection_name!='' else collections[0]
    print(collection_name)

    table = db[collection_name]

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

    province_msg = '| 序号 | 省份 | 设备数 | 阴性数 | 阳性数 | 无效数 | 检测总量 |\n| ---- | ---- | ------ | ------ | ------ | ------ | -------- |\n'
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

    batch_msg = '| 批次号 | 阴性数 | 阳性数 | 无效数 | 检测总量 |\n| ---- | ---- | ------ | ------ | ------  |\n ' 
    total = [0] * 4
    for key in d_batch.keys():
        # print(key)
        # print(d_batch[key])
        batch_msg += '|' + str(key) + '|' + str(d_batch[key].yin) + '|' +  str(d_batch[key].yang) + '|' +  str(d_batch[key].wu) + '|' + str( d_batch[key].wu +  d_batch[key].yang + d_batch[key].yin) + '|\n' 
        total[0] += d_batch[key].yin
        total[1] += d_batch[key].yang
        total[2] += d_batch[key].wu
    total[3] = sum(total[:-1])
    batch_msg += '| 总计|' + '|'.join([str(i) for i in total]) + '|'
    print(batch_msg)

    contest = {
        'collection_name': collection_name,
        'collections' : collections,
        'province_msg': province_msg,
        'batch_msg': batch_msg,
    }
    return render(request, 'week.html', contest)

def days_view(request):
    # values = [120, 200, 150, 80, 70, 110, 130]
    current_parent_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
    CONFIG_FILE_PATH = os.path.join(current_parent_dir, 'conf.ini')
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    TABLE = config.get('database', 'TABLE')
    DB = config.get('database', 'DB')
    client = pymongo.MongoClient('localhost')
    db = client[DB]
    table = db[TABLE]
    days = res_7days(table)
    print(days)
    context = {
        'values': days
    }
    return render(request, 'days.html', context)


def weeks_view(request):
    current_parent_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
    CONFIG_FILE_PATH = os.path.join(current_parent_dir, 'conf.ini')
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    TABLE = config.get('database', 'TABLE')
    DB = config.get('database', 'DB')
    client = pymongo.MongoClient('localhost')
    db = client[DB]
    table = db[TABLE]
    weeks = res_7weeks(table)
    print(weeks)
    context = {
        'values': weeks
    }
    return render(request, 'weeks.html', context)


def months_view(request):
    current_parent_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
    CONFIG_FILE_PATH = os.path.join(current_parent_dir, 'conf.ini')
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    TABLE = config.get('database', 'TABLE')
    DB = config.get('database', 'DB')
    client = pymongo.MongoClient('localhost')
    db = client[DB]
    table = db[TABLE]
    weeks = res_7weeks(table)
    print(weeks)
    context = {
        'values': weeks
    }
    return render(request, 'months.html', context)