# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import warnings
import scrapy


class PachongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    RecordID = scrapy.Field() 
    ItemID  = scrapy.Field() 
    BatchID = scrapy.Field() 
    sSampleID= scrapy.Field() 
    sItemName= scrapy.Field() 
    sBatchCode= scrapy.Field() 
    sTime= scrapy.Field() 
    Concentration  = scrapy.Field() 
    Judge= scrapy.Field() 
    CValue= scrapy.Field() 
    TValue1 = scrapy.Field() 
    TValue2 = scrapy.Field() 
    TValue3 = scrapy.Field() 
    SNcode = scrapy.Field()
    sTimeNumber = scrapy.Field()
    points = scrapy.Field()
    address = scrapy.Field()
    data_bight = scrapy.Field()
    create_time = scrapy.Field() 
    gender = scrapy.Field()
    place = scrapy.Field()
    cons1 = scrapy.Field()
    cons2 = scrapy.Field()
    cons3 = scrapy.Field()
    conclusion1 = scrapy.Field()
    conclusion2 = scrapy.Field()
    conclusion3 = scrapy.Field()
    conclusion1 = scrapy.Field()
    judge_res = scrapy.Field()
    warning = scrapy.Field()
