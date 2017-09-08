#-*- coding: utf-8 -*-
from pymongo import MongoClient
import xlrd
from datetime import timedelta
import datetime

conn = MongoClient('localhost', 27017)
db = conn.GA
watches = db.watches

def to_date(rb, date):
  year, month, day, hour, minute, second = xlrd.xldate_as_tuple(date, rb.datemode)
  return datetime.date(year, month, day)

def get_horizon(date):
    report_day = datetime.datetime.today().date()
    return (report_day-date).days

#for elem in watches.find({"name": u'Здравствуйте, меня зовут Дорис'}):
#    print elem["name"], elem["LG"],elem["Samsung"], elem["Android"], elem["iOS"]
#watches.delete_many({"name": "1+1"})


#Здравствуйте, меня зовут Дорис
#Дивергент, глава 3: За стеной
#Человек, который изменил всё
#1+1
#14+

"""
rb = xlrd.open_workbook('bearing.xlsx')
sheet = rb.sheet_by_index(0)
for rownum in range(sheet.nrows-1):
    row = sheet.row_values(rownum+1)

    if type(row[0]) == float:
        code = str(int(row[0]))
    else:
        code = row[0]

    if type(row[1]) == float:
        id = str(int(row[1]))
    else:
        id = row[1]

    print code, id
    watches.update_many({"id": id, "date": "2016-12-21"}, {"$set": {"code": code}})
"""