#-*- coding: utf-8 -*-
import xlrd
from datetime import timedelta
import datetime
from pymongo import MongoClient
import pprint
from apiclient.discovery import build
import httplib2
import xlwt
from oauth2client.service_account import ServiceAccountCredentials
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = 'client_secrets.p12'
SERVICE_ACCOUNT_EMAIL = 'eugene@python-149108.iam.gserviceaccount.com'


"""платформы для отчетов (для smart TV данные по User_ID)"""
Platforms = {"LG": "96890573", "Samsung": "96900905", "Android": "125654904", "iOS": "125643516"}


"""преобразуем дату из excel"""
def to_date(rb, date):
  year, month, day, hour, minute, second = xlrd.xldate_as_tuple(date, rb.datemode)
  return datetime.date(year, month, day)


"""connecting to mongodb"""
def connect_to_database():
    conn = MongoClient('localhost', 27017)
    db = conn.GA
    return db


"""получаем информацию по фильмам из опорного файла"""
def get_films():

  Collections = {}
  Promo = []
  New = []
  Recommended = []
  Selected = []
  New_year = []

  rb = xlrd.open_workbook('new_year.xlsx')
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


"""cмотрим горизонт наблюдения"""
def get_date_range(since):
  date_range = []
  now = since
  report_day = datetime.datetime.today().date() - timedelta(days=1)
  while now <= report_day:
    date_range.append(now)
    now += timedelta(days=1)
  return date_range

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



"""попробовать получить информацию по фильму индивидуально"""
def give_a_try(film, date):
  print film

  try:
      query = query_builder("96890573", date, date, "watches", "watch", "@" + film)
      print query
      analytics = initialize_analyticsreporting()
      response = get_report(analytics, query)
      x, y = get_response(response)

      if y == []:
        print date, 0
      else:
        print date, y
  except:
      print "wtf"


"""выполняем нужный запрос к полученной базе"""
def query_database(db, Collections):
    watches_database = db.watches
    watches_database.delete_many({"name": "Гипнотизер", "date": "2016-11-30"})


"""получаем ядро базы, дальше будем только обновлять его - плоская структура (SQL-like)"""
def easy_structure(Collections, db):
    watches_database = db.watches

    new_record = {}
    for collection in Collections:
        print collection

        for film in Collections[collection]:
            print film["name"]

            if film["regex"] != u'':
                film_name = "@" + film["regex"]
            else:
                film_name = "=" + film["name"]


            for day in get_date_range(film["date"]):
                new_record["date"] = day.strftime("%Y-%m-%d")

                for platform in Platforms:

                    if platform not in ["iOS", "Android"]:
                        eventCategory = "watches"
                        eventAction = "watch"
                    else:
                        eventCategory = "Watches"
                        eventAction = "Watch"

                    query = query_builder(Platforms[platform], day.strftime("%Y-%m-%d"), day.strftime("%Y-%m-%d"), eventCategory, eventAction, film_name)
                    analytics = initialize_analyticsreporting()

                    try:
                        response = get_report(analytics, query)
                        x, y = get_response(response)

                        if y == []:
                            print platform, day, 0
                            new_record[platform] = 0

                        else:
                            print platform, day, y[0]
                            new_record[platform] = y[0]

                    except:
                        print "error"

                new_record["name"] = film["name"]
                new_record["id"] = film["id"]
                new_record["kp_id"] = film["kp_id"]
                new_record["code"] = film["code"]
                watches_database.save(new_record)
                new_record = {}


"""обновляем информацию в базе"""
def update_easy_structure(Collections, db):
    watches_database = db.watches

    for collection in Collections:
        print collection
        for film in Collections[collection]:
            print film["name"]

            for day in get_date_range(film["date"]):

                if watches_database.find({"name": film["name"], "date": day.strftime("%Y-%m-%d")}).count() == 1:
                    pass
                else:
                    new_record = {}
                    new_record["date"] = day.strftime("%Y-%m-%d")

                    if film["regex"] != u'':
                        if type(film["regex"]) == float:
                            film_name = "@" + str(int(film["regex"]))
                        else:
                            film_name = "@" + film["regex"]
                    else:
                        film_name = "=" + film["name"]

                    for platform in Platforms:

                        if platform not in ["iOS", "Android"]:
                            eventCategory = "watches"
                            eventAction = "watch"
                        else:
                            eventCategory = "Watches"
                            eventAction = "Watch"

                        query = query_builder(Platforms[platform], day.strftime("%Y-%m-%d"), day.strftime("%Y-%m-%d"), eventCategory, eventAction, film_name)
                        analytics = initialize_analyticsreporting()

                        try:
                            response = get_report(analytics, query)
                            x, y = get_response(response)

                            if y == []:
                                print platform, day, 0
                                new_record[platform] = 0

                            else:
                                print platform, day, y[0]
                                new_record[platform] = y[0]

                        except:
                            print "error"

                    new_record["name"] = film["name"]
                    new_record["id"] = film["id"]
                    new_record["kp_id"] = film["kp_id"]
                    new_record["code"] = film["code"]
                    watches_database.save(new_record)


Collections = get_films()
pprint.pprint(Collections)
#db = connect_to_database()
#update_easy_structure(Collections, db)


