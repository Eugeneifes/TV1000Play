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
Platforms = {"LG": "116060770", "Samsung": "116048361", "Android": "125654904", "iOS": "125643516"}

regular = {u'Дивергент, глава 3: За стеной': "За стеной",
           u'Здравствуйте, меня зовут Дорис': "меня зовут Дорис",
           u'Человек, который изменил всё': "который изменил всё",
           u'14+ (L)': "14"}


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
        "filtersExpression": "ga:eventCategory==" + eventCategory + ";ga:eventAction==" + eventAction + ";ga:eventLabel=" + film
      }
    ]
  }
  return query


"""преобразуем дату из excel"""
def to_date(rb, date):
  year, month, day, hour, minute, second = xlrd.xldate_as_tuple(date, rb.datemode)
  return datetime.date(year, month, day)


"""получаем информацию по фильмам из опорного файла"""
def get_films():

  Collections = {}
  Promo = []
  New = []
  Recommended = []
  Selected = []
  New_year = []

  rb = xlrd.open_workbook('bearing.xlsx')
  sheet = rb.sheet_by_index(0)
  for rownum in range(sheet.nrows-1):
    row = sheet.row_values(rownum+1)
    film = {}

    if type(row[0]) == float:
        film["code"] = str(int(row[0]))
    else:
        film["code"] = str(row[0])

    if type(row[1]) == float:
        film["id"] = str(int(row[1]))
    else:
        film["id"] = str(row[1])

    if type(row[2]) == float:
        film["kp_id"] = str(int(row[2]))
    else:
        film["kp_id"] = str(row[2])


    film["name"] = row[4]

    if row[6] != "":
        film["regex"] = row[6]
    else:
        film["regex"] = ""

    print row[3], row[7]
    film["date"] = to_date(rb, row[7])

    if row[8] == u'Промо':
        Promo.append(film)
    if row[8] == u'Новое':
        New.append(film)
    if row[8] == u'Рекомендуемое':
        Recommended.append(film)
    if row[8] == u'Подборки':
        Selected.append(film)
    if row[8] == u'Новый год 2017':
        New_year.append(film)


  Collections["Promo"] = Promo
  Collections["New"] = New
  Collections["Recommended"] = Recommended
  Collections["Selected"] = Selected
  Collections["New_year"] = New_year

  return Collections


"""сколько фильмов в коллекции"""
def count_films(collection):
  return len(Collections[collection].keys())


"""cмотрим горизонт наблюдения"""
def get_horizon():
  date_range = []
  horizon = datetime.datetime.today().date()

  for collection in Collections.keys():
    for film in Collections[collection]:
      if film["date"] < horizon:
        horizon = film["date"]
  now = horizon
  today = datetime.datetime.today().date() - timedelta(days=1)
  while now <= today:
    date_range.append(now)
    now += timedelta(days=1)
  return date_range


"""вывести фильмы, которые не ищутся"""
def to_correct(Collections):
  for collection in Collections.keys():
    for film in Collections[collection]:
      try:
        date = datetime.datetime.today().date().strftime("%Y-%m-%d")
        query = query_builder("116060770", date, date, "watches", "film_watch_25", "="+film[0])
        analytics = initialize_analyticsreporting()
        response = get_report(analytics, query)
        x, y = get_response(response)
      except:
        print "wtf"
        print film[0]


"""выполняем нужный запрос к полученной базе"""
def query_database(db, Collections):
    watches_database = db.watches

    for collection in Collections:
        for film in Collections[collection]:
            watches_database.delete_many({"name": film[0], "date": "2016-12-05"})


"""попробовать получить информацию по фильму индивидуально"""
def give_a_try(film, date_range):
  print film
  for date in date_range:
    try:
      query = query_builder("116060770", date.strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d"), "watches", "film_watch_25", "@" + film)
      analytics = initialize_analyticsreporting()
      response = get_report(analytics, query)
      x, y = get_response(response)

      if y == []:
        print date, 0
      else:
        print date, y
    except:
      print "wtf"


"""формирование отчета из базы данных"""
def report():
  watches_database = db.watches

  wb = xlwt.Workbook()
  ws = wb.add_sheet('Watches')
  platform_row = 1
  date_col = 2
  film_row = 1
  data_col = 2
  film_appear_style = xlwt.easyxf('pattern: pattern solid, fore_colour red;')

  for date in date_range:
    ws.write(0, date_col, label=date.strftime("%Y-%m-%d"))
    date_col += 1

  for collection in Collections.keys():
    for film in Collections[collection]:

      ws.write_merge(r1=film_row, r2=(film_row + 3), c1=0, c2=0, label=film["name"])
      print film["name"]

      for platform in Platforms.keys():
        print platform
        ws.write(platform_row, 1, label=platform)

        for date in date_range:
          for doc in watches_database.find({"name": film["name"], "date": date.strftime("%Y-%m-%d")}):
            if date == film["date"]:
              ws.write(platform_row, data_col, doc[platform], style=film_appear_style)
            else:
              ws.write(platform_row, data_col, doc[platform])
          data_col+=1
        data_col=2
        platform_row += 1
      film_row += 4
    wb.save('Watches.xls')


Collections = get_films()
pprint.pprint(Collections)
#date_range = get_horizon()
#db = connect_to_database()
#report()
#query_database(db, Collections)



films = ["Табу", "Дедпул", "Варкрафт", "Смотрите День Сурка", "Сноуден", "Кингсглейв: Последняя фантазия XV", "Гений", "Изумрудный город", "Выживший", "Angry Birds в кино"]