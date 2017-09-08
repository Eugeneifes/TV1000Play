#-*- coding: utf-8 -*-

from apiclient.discovery import build
import httplib2
import json
import io
from datetime import date, timedelta
import sys
import requests
from oauth2client.service_account import ServiceAccountCredentials
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = 'client_secrets.p12'
SERVICE_ACCOUNT_EMAIL = 'eugene@python-149108.iam.gserviceaccount.com'


"""платформы для отчетов (для smart TV (все данные по сайту))"""
Platforms = {"LG": "96890573", "Samsung": "96900905"}


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
def query_builder_with_label(VIEW_ID, startdate, enddate, eventCategory, eventAction, eventLabel):
  query = {
    'reportRequests': [
      {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': startdate, 'endDate': enddate}],
        'metrics': [{'expression': 'ga:totalEvents'}],
        "filtersExpression": "ga:eventCategory==" + eventCategory + ";ga:eventAction==" + eventAction + ";ga:eventLabel==" + eventLabel
      }
    ]
  }
  return query

"""формируем запрос к GA"""
def query_builder_without_label(VIEW_ID, startdate, enddate, eventCategory, eventAction):
  query = {
    'reportRequests': [
      {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': startdate, 'endDate': enddate}],
        'metrics': [{'expression': 'ga:totalEvents'}],
        "filtersExpression": "ga:eventCategory==" + eventCategory + ";ga:eventAction==" + eventAction
      }
    ]
  }
  return query


"""формируем запрос к GA"""
def query_builder_sessions(VIEW_ID, date):
  query = {
    'reportRequests': [
      {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': date, 'endDate': date}],
        'metrics': [{'expression': 'ga:sessions'}],
      }
    ]
  }
  return query


"""формируем запрос к GA"""
def query_builder_users(VIEW_ID, date):
  query = {
    'reportRequests': [
      {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': date, 'endDate': date}],
        'metrics': [{'expression': 'ga:users'}],
      }
    ]
  }
  return query


"""попробовать получить информацию по фильму индивидуально"""
def give_a_try(date):
  query = query_builder("96890573", date, date, "new_Mainpage", "random_film_click")
  print query
  analytics = initialize_analyticsreporting()
  response = get_report(analytics, query)
  x, y = get_response(response)

  if y == []:
    print date, 0
  else:
    print date, y



def get_editor_collection_clicks(key, date, name):
  query = query_builder_with_label(Platforms[key], date, date, "new_Mainpage", "editor_collection_click", name)
  analytics = initialize_analyticsreporting()
  response = get_report(analytics, query)
  x, y = get_response(response)
  if y == []:
    print key, name, date, 0
    return 0
  else:
    print key, name, date, y
    return y[0]




def get_series_clicks(key, date):

  query = query_builder_without_label(Platforms[key], date, date, "Series", "series_anchor_click")
  analytics = initialize_analyticsreporting()
  response = get_report(analytics, query)
  x, y = get_response(response)
  if y == []:
    print key, u'Сериалы', date, 0
    return 0
  else:
    print key, u'Сериалы', date, y
    return y[0]



def get_continue_watch_clicks(key, date):

  query = query_builder_without_label(Platforms[key], date, date, "Series", "continue_watch_click")
  analytics = initialize_analyticsreporting()
  response = get_report(analytics, query)
  x, y = get_response(response)
  if y == []:
    print key, u'Продолжайте просмотр', date, 0
    return 0
  else:
    print key, u'Продолжайте просмотр', date, y
    return y[0]


def get_tile_clicks(key, date, name):
  query = query_builder_without_label(Platforms[key], date, date, "new_Mainpage", name)
  analytics = initialize_analyticsreporting()
  response = get_report(analytics, query)
  x, y = get_response(response)
  if y == []:
    print key, name, date, 0
    return 0
  else:
    print key, name, date, y
    return y[0]


def get_sessions(key, date):
  query = query_builder_sessions(Platforms[key], date)
  analytics = initialize_analyticsreporting()
  response = get_report(analytics, query)
  x, y = get_response(response)
  if y == []:
    print key, "sessions", date, 0
    return 0
  else:
    print key, "sessions", date, y
    return y[0]


def get_users(key, date):
  query = query_builder_users(Platforms[key], date)
  analytics = initialize_analyticsreporting()
  response = get_report(analytics, query)
  x, y = get_response(response)
  if y == []:
    print key, "users", date, 0
    return 0
  else:
    print key, "users", date, y
    return y[0]



if __name__ == "__main__":

  today = date.today() - timedelta(1)
  yesterday = date.today() - timedelta(2)

  result = []
  r = requests.get("http://stats-testing.herokuapp.com/ga")
  dict = json.loads(r.text)
  print(dict)

  for elem in dict:

    if 'ga_name' not in elem.keys():

      if elem['name'] == u'Сериалы':
        statistics = {}
        statistics["name"] = u'Сериалы'
        statistics["id"] = elem['id']
        statistics["today_lg"] = get_series_clicks("LG", today.strftime("%Y-%m-%d"))
        statistics["yesterday_lg"] = get_series_clicks("LG", yesterday.strftime("%Y-%m-%d"))
        statistics["today_samsung"] = get_series_clicks("Samsung", today.strftime("%Y-%m-%d"))
        statistics["yesterday_samsung"] = get_series_clicks("Samsung", yesterday.strftime("%Y-%m-%d"))
        result.append(statistics)

      elif elem['name'] == u'Продолжайте просмотр':
        statistics = {}
        statistics["name"] = u'Продолжайте просмотр'
        statistics["id"] = elem['id']
        statistics["today_lg"] = get_continue_watch_clicks("LG", today.strftime("%Y-%m-%d"))
        statistics["yesterday_lg"] = get_continue_watch_clicks("LG", yesterday.strftime("%Y-%m-%d"))
        statistics["today_samsung"] = get_continue_watch_clicks("Samsung", today.strftime("%Y-%m-%d"))
        statistics["yesterday_samsung"] = get_continue_watch_clicks("Samsung", yesterday.strftime("%Y-%m-%d"))
        result.append(statistics)

      else:
        statistics = {}
        statistics["name"] = elem['name']
        statistics["id"] = elem['id']
        statistics["today_lg"] = get_editor_collection_clicks("LG", today.strftime("%Y-%m-%d"), elem['name'])
        statistics["yesterday_lg"] = get_editor_collection_clicks("LG", yesterday.strftime("%Y-%m-%d"), elem['name'])
        statistics["today_samsung"] = get_editor_collection_clicks("Samsung", today.strftime("%Y-%m-%d"), elem['name'])
        statistics["yesterday_samsung"] = get_editor_collection_clicks("Samsung", yesterday.strftime("%Y-%m-%d"), elem['name'])
        result.append(statistics)

    else:

      if elem['name'] == u'Лучшее':
        statistics = {}
        statistics["name"] = elem['name']
        statistics["id"] = elem['id']
        statistics["today_lg"] = get_editor_collection_clicks("LG", today.strftime("%Y-%m-%d"), elem['name'])
        statistics["yesterday_lg"] = get_editor_collection_clicks("LG", yesterday.strftime("%Y-%m-%d"), elem['name'])
        statistics["today_samsung"] = get_editor_collection_clicks("Samsung", today.strftime("%Y-%m-%d"), elem['name'])
        statistics["yesterday_samsung"] = get_editor_collection_clicks("Samsung", yesterday.strftime("%Y-%m-%d"), elem['name'])
        result.append(statistics)

      else:
        statistics = {}
        statistics["name"] = elem['name']
        statistics["id"] = elem['id']
        statistics["today_lg"] = get_tile_clicks("LG", today.strftime("%Y-%m-%d"), elem['ga_name'])
        statistics["yesterday_lg"] = get_tile_clicks("LG", yesterday.strftime("%Y-%m-%d"), elem['ga_name'])
        statistics["today_samsung"] = get_tile_clicks("Samsung", today.strftime("%Y-%m-%d"), elem['ga_name'])
        statistics["yesterday_samsung"] = get_tile_clicks("Samsung", yesterday.strftime("%Y-%m-%d"), elem['ga_name'])
        result.append(statistics)


  statistics={}
  statistics["lg_sessions_today"] = get_sessions("LG", today.strftime("%Y-%m-%d"))
  statistics["lg_sessions_yesterday"] = get_sessions("LG", yesterday.strftime("%Y-%m-%d"))
  statistics["lg_users_today"] = get_users("LG", today.strftime("%Y-%m-%d"))
  statistics["lg_users_yesterday"] = get_users("LG", yesterday.strftime("%Y-%m-%d"))

  statistics["samsung_sessions_today"] = get_sessions("Samsung", today.strftime("%Y-%m-%d"))
  statistics["samsung_sessions_yesterday"] = get_sessions("Samsung", yesterday.strftime("%Y-%m-%d"))
  statistics["samsung_users_today"] = get_users("Samsung", today.strftime("%Y-%m-%d"))
  statistics["samsung_users_yesterday"] = get_users("Samsung", yesterday.strftime("%Y-%m-%d"))
  result.append(statistics)

  with io.open('tiles_clicks.txt', 'w', encoding='utf8') as outfile:
    outfile.write(json.dumps(result, outfile, ensure_ascii=False))


#active_tiles = ["editor_collection_click", "scroll_right", "scroll_left", "hurry_up_click", "films_you_like_click", "random_film_click", "genres_click"]






