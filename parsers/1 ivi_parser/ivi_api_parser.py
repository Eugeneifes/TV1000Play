# -*- coding: utf-8 -*-

import requests
import json
import io
import pprint
from bs4 import BeautifulSoup


def parse_payment_options(id):
    r = requests.get("https://api.ivi.ru/mobileapi/billing/v1/purchase/content/options/?id="+str(id)+"&app_version=870&session=a1bdfd8e752889640_1506677244OItLVx6M1P20xNRuNPFJ1w")
    dict = json.loads(r.content)
    options = []

    for purchase_option in dict['result']['purchase_options']:
        option = {}

        if purchase_option['payment_options'][0]['purchase_params']['_quality']:
            if purchase_option['payment_options'][0]['purchase_params']['_ownership_type'] == 'eternal':

                option["ownership_type"] = "EST"
                option["price"] = purchase_option['payment_options'][0]['purchase_params']['_price'].split(".")[0]
                option["quality"] = purchase_option['payment_options'][0]['purchase_params']['_quality']
                options.append(option)

            else:
                option["ownership_type"] = "TVOD"
                option["price"] = purchase_option['payment_options'][0]['purchase_params']['_price'].split(".")[0]
                option["quality"] = purchase_option['payment_options'][0]['purchase_params']['_quality']
                options.append(option)

    return options


def parse_collections(elem, object_type, category):

    r = requests.get("https://www.ivi.ru/watch/" + elem['hru'])
    soup = BeautifulSoup(r.text)
    for item in soup.find("ul", class_='inner-nav', id='group-list').find_all("li"):
        r = requests.get("https://api.ivi.ru/mobileapi/videofromcompilation/v5/?id=" + str(elem['id']) + "&from=" + item.a['data-from'] + "&to=" + item.a['data-to'] + "&app_version=870")
        dict = json.loads(r.content)
        if dict['result']:
            parse_item(dict['result'][0], compilation_name=item.text, object_type=object_type, category=category)


def parse_serials(elem, object_type, category):

    for season in elem["seasons"]:
        r = requests.get("https://api.ivi.ru/mobileapi/videofromcompilation/v5/?id=" + str(elem['id']) + "&season=" + str(season) + "&app_version=870")
        dict = json.loads(r.content)
        if dict['result']:
            parse_item(dict['result'][0], season=season, object_type=object_type, category=category)


def parse_compilations(elem, object_type, category):
    if elem["seasons"] == []:

        parse_collections(elem, object_type, category)

    else:
        parse_serials(elem, object_type, category)


def print_it(item):

    if item['business_type']:
        if item['object_type'] == "compilation":
            if item["season"]:
                print item['id'], item['compilation_title'], item['season'], item['business_type']

            else:
                print item['id'], item['compilation_title'], item['compilation_name'], item['business_type']

        elif item['object_type'] == "video":
            print item['id'], item['title'], item['business_type']

    else:
        for content_paid_type in item['content_paid_types']:

            if item['object_type'] == "compilation":
                if item["season"]:
                    print item['id'], item['compilation_title'], item['season'], content_paid_type['ownership_type'], content_paid_type['price'], content_paid_type['quality']

                else:
                    print item['id'], item['compilation_title'], item['compilation_name'], content_paid_type['ownership_type'], content_paid_type['price'], content_paid_type['quality']

            elif item['object_type'] == "video":
                print item['id'], item['title'], content_paid_type['ownership_type'], content_paid_type['price'], content_paid_type['quality']




def get_content_fields(elem, compilation_name, season, business_type, content_paid_types, object_type, category):

    item = {}

    item['object_type'] = object_type
    item['category'] = category
    item['business_type'] = business_type
    item['content_paid_types'] = content_paid_types


    item['duration'] = elem['duration']

    try:
        item['year'] = elem['year']
    except:
        item['year'] = ''

    item['title'] = elem['title']
    item['orig_title'] = elem['orig_title']
    item['release_date'] = elem['release_date']
    item['restrict'] = elem['restrict']

    '''for serials'''
    try:
        item['episode'] = elem['episode']
    except:
        item['episode'] = ''

    try:
        item['compilation_title'] = elem['compilation_title']
    except:
        item['compilation_title'] = ''


    item['season'] = season
    item['compilation_name'] = compilation_name


    '''other fields'''
    try:
        item['kp_rating'] = elem['kp_rating']
    except:
        item['kp_rating'] = ''

    try:
        item['ivi_rating'] = elem['ivi_rating']
    except:
        item['ivi_rating'] = ''

    try:
        item['imdb_rating'] = elem['imdb_rating']
    except:
        item['imdb_rating'] = ''


    item['id'] = elem['id']

    try:
        print_it(item)
    except:
        pass

    database.append(item)

    with io.open('ivi_cartoon_database.txt', 'w', encoding='utf8') as outfile:
        outfile.write(json.dumps(database, outfile, ensure_ascii=False))



def parse_item(elem, object_type, category, compilation_name='', season=''):

    for business_type in elem['content_paid_types']:

        if business_type == u'TVOD' or business_type == u'EST':
            payment_options = parse_payment_options(elem['id'])

            if {"id": elem["id"], "payment_options": payment_options} not in memory:

                memory.append({"id": elem["id"], "payment_options": payment_options})
                get_content_fields(elem, compilation_name, season, '', payment_options, object_type, category)

        else:
            get_content_fields(elem, compilation_name, season, business_type, '', object_type, category)



database = []
memory = []

'''
Категории:
14 - Фильмы
15 - Сериалы
16 - Телешоу
17 - Мультфильмы
'''

categories = {"cartoon": 17}

for category in categories.keys():

    '''за один запрос api ivi отдает максимум 100 элементов (следовательно делаем смещение с шагом в 100)'''
    start = 0
    end = 99

    r = requests.get("https://api.ivi.ru/mobileapi/catalogue/v5/?app_version=870&from="+str(start)+"&to="+str(end)+"&category="+str(categories[category]))
    dict = json.loads(r.content)


    '''критерий остановки парсера  - возвращение пустого массива (фильмов больше нет)'''
    while dict['result'] != []:
        for elem in dict['result']:

            '''есть два типа объектов: video (единица) - фильм/мультильм; compilation(подборка) - сериал/шоу/многосерийный фильм'''
            if elem['object_type'] == 'video':
                result = parse_item(elem, object_type="video", category=category)

            if elem['object_type'] == 'compilation':
                result = parse_compilations(elem, object_type="compilation", category=category)


        start += 100
        end += 100
        r = requests.get("https://api.ivi.ru/mobileapi/catalogue/v5/?app_version=870&from=" + str(start) + "&to=" + str(end) + "&category=" + str(categories[category]))
        dict = json.loads(r.content)












