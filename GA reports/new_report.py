#-*- coding: utf-8 -*-

import argparse
import xlwt
import xlrd
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from pymongo import MongoClient
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
import datetime
from datetime import timedelta
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = 'client_secrets.p12'
SERVICE_ACCOUNT_EMAIL = 'eugene@python-149108.iam.gserviceaccount.com'


"""платформы для отчетов"""
Platforms = {"LG": "96890573", "Samsung": "96900905", "Android": "125654904", "iOS": "125643516"}


"""инициализация клиента GA Reporting API"""
def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_p12_keyfile(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)
  http = credentials.authorize(httplib2.Http())
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)
  return analytics


"""получить отчет по запросу"""
def get_report(analytics, query):
  return analytics.reports().batchGet(body=query).execute()


"""connecting to mongodb"""
def connect_to_database():
    conn = MongoClient()
    conn = MongoClient('localhost', 27017)
    db = conn.GA
    return db

"""получаем и парсим ответ от сервера GA"""
def get_response(response):
  x_mass = []
  y_mass = []
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])


      for header, dimension in zip(dimensionHeaders, dimensions):
        x_mass.append(int(dimension))


      for i, values in enumerate(dateRangeValues):
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          y_mass.append(int(value))

  return x_mass, y_mass


"""формируем запрос к GA"""
def query_builder(VIEW_ID, startdate, enddate, eventCategory, eventAction, film):
  query = {
    'reportRequests': [
      {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': startdate, 'endDate': enddate}],
        'metrics': [{'expression': 'ga:totalEvents'}],
        "filtersExpression": "ga:eventCategory==" + eventCategory + ";ga:eventAction==" + eventAction + ";ga:eventLabel==" + film
      }
    ]
  }
  return query


"""преобразуем дату из excel"""
def to_date(rb, date):
  year, month, day, hour, minute, second = xlrd.xldate_as_tuple(date, rb.datemode)
  return datetime.date(year, month, day)





"""cмотрим горизонт наблюдения"""
def get_horizon():
  date_range = []
  now = datetime.datetime.today().date() - timedelta(days=33)
  today = datetime.datetime.today().date() - timedelta(days=1)
  while now <= today:
    date_range.append(now)
    now += timedelta(days=1)
  return date_range




"""формирование отчета"""
def report():

  wb = xlwt.Workbook()
  ws = wb.add_sheet('Watches')
  platform_row = 1
  date_col = 2
  film_row = 1
  data_col = 2


  for date in date_range:
    ws.write(0, date_col, label=date.strftime("%Y-%m-%d"))
    date_col += 1

  for film in films:

      ws.write_merge(r1=film_row, r2=(film_row + 3), c1=0, c2=0, label=film)
      print film

      for platform in Platforms:
          print platform

          if platform not in ["iOS", "Android"]:
              eventCategory = "watches"
              eventAction = "watch"
          else:
              eventCategory = "Watches"
              eventAction = "Watch"

          ws.write(platform_row, 1, label=platform)

          for date in date_range:

              query = query_builder(Platforms[platform], date.strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d"), eventCategory, eventAction, film)
              analytics = initialize_analyticsreporting()


              response = get_report(analytics, query)
              x, y = get_response(response)

              if y == []:
                  print platform, date, 0
                  ws.write(platform_row, data_col, 0)

              else:
                  print platform, date, y[0]
                  ws.write(platform_row, data_col, y[0])


              data_col += 1
              wb.save('Watches.xls')
          data_col = 2
          platform_row += 1

      film_row += 4
  wb.save('Watches.xls')


films = [u"Варкрафт", u"Дэдпул", u"Табу", u"Гримм",  u"Выживший", u"Отмель", u"Изумрудный город",  u"Омерзительная восьмерка", u"Ледокол", u"007: СПЕКТР"]
date_range = get_horizon()
report()


