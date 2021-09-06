import pymongo
# RecordID, SNcode, ItemID ,BatchID ,sSampleID ,ItemName ,sBatchCode ,sTimeNumber ,cons1 ,conclusion1 ,CValue ,TValue1 ,cons2 ,cons3 ,conclusion2 ,conclusion3 ,TValue2 ,TValue3 ,place
# 序号	仪器序列号	项目号	批次号	样品编号	项目名称	批次名称	测试时间	浓度1	结论1	C值	T1值	浓度2	浓度3	结论2	结论3	T2值	T3值	详细地址																																																																																																																																																																																																																																																																																																																																											
client = pymongo.MongoClient('localhost')
db = client['test']
table = db['hel']
collections = table.find({})
with open('test.csv','w', encoding='gbk') as f:
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
        print(SNcode)
        l = [RecordID, SNcode, ItemID ,BatchID ,sSampleID ,ItemName ,sBatchCode ,sTimeNumber ,cons1 ,conclusion1 ,CValue ,TValue1 ,cons2 ,cons3 ,conclusion2 ,conclusion3 ,TValue2 ,TValue3 ,'',address]
        for ele in l:
                print(str(ele))
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
        
