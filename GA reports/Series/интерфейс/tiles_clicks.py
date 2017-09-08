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
Platforms = {"LG": "96890573", "Samsung": "96900905", "Philips": "102311357"}


"""инициализация клиента GA Reporting API"""
def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_p12_keyfile(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)
  http = credentials.authorize(httplib2.Http())
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)
  return analytics


"""получить отчет по запросу"""
def get_report(analytics, query):
  return analytics.reports().batchGet(body=query).execute()


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
        "filtersExpression": "ga:eventCategory==" + eventCategory + ";ga:eventAction==" + eventAction + ";ga:eventLabel=" + film
      }
    ]
  }
  return query


"""преобразуем дату из excel"""
def to_date(rb, date):
  year, month, day, hour, minute, second = xlrd.xldate_as_tuple(date, rb.datemode)
  return datetime.date(year, month, day)



"""формирование отчета из базы данных"""
def report(series):


  wb = xlwt.Workbook()
  ws = wb.add_sheet('Watches')
  date_col = 3
  film_row = 1
  data_col = 3


  for date in date_range:
    ws.write(0, date_col, label=date.strftime("%Y-%m-%d"))
    date_col += 1


  for eventAction in actions:
      for serie in series:
        for platform in Platforms.keys():
            print platform
            ws.write(film_row, 0, label=eventAction)
            ws.write(film_row, 1, label=serie.decode("utf-8"))
            ws.write(film_row, 2, label=platform)


            for date in date_range:
                query = query_builder(Platforms[platform], date.strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d"), "SeriesCards", eventAction, "@" + serie)
                analytics = initialize_analyticsreporting()
                response = get_report(analytics, query)
                x, y = get_response(response)

                if y == []:
                    print date, 0
                    ws.write(film_row, data_col, 0)
                else:
                    print date, y
                    ws.write(film_row, data_col, y[0])


                data_col += 1
            film_row += 1
            data_col = 3
            wb.save('Watches.xls')


series = ["Табу", "Изумрудный город", "Гримм", "Настоящий гений", "Черный список. Искупление"]
actions = ["film_card", "story", "trailer", "choose_season", "additional", "series_click"]
date_range = []
first_day = datetime.datetime(2017, 1, 1)
last_day = datetime.datetime(2017, 3, 15)
now = first_day

while now <= last_day:
    date_range.append(now)
    now += timedelta(days=1)

report(series)