# -*- coding: utf-8 -*-
import requests
import json
import pprint
import time
import datetime
import io

'''Получаем список категорий, по которым пройдется парсер'''
r = requests.get("https://sa-web.okko.tv/screenapi/v1/noauth/categories/web/1?")
collection_dict = json.loads(r.content)


def get_countries(countries):
    countries_mass = []

    for country in countries['items']:
        countries_mass.append(country['element']['name'])

    #print ", ".join(countries_mass)
    return countries_mass



def get_genres(genres):
    genres_mass = []

    for genre in genres['items']:
        genres_mass.append(genre['element']['name'])

    #print ", ".join(genres_mass)
    return genres_mass



def parse_pay_type(pay_types):

    pay_types_mass = []

    for pay_type in pay_types['items']:
        if pay_type['type'] == 'UPGRADE':
            pass
            #print pay_type['price']['value'], pay_type['consumptionMode'], pay_type['qualities'], pay_type['type'], pay_type['fromQuality'], pay_type['fromConsumptionMode']
        else:
            pay_types_mass.append({"price": pay_type['price']['value'], "business_type": pay_type['consumptionMode'], "quality": pay_type['qualities']})
    return pay_types_mass



films = []
for item in collection_dict['element']['collectionItems']['items']:

    alias = item['element']['alias']
    type = item['element']['type']

    '''Пробный запрос для определения количества элементов в подборке (полученный результат будет передан в параметре limit)'''
    r = requests.get("https://sa-web.okko.tv/screenapi/v1/noauth/collection/web/1?elementAlias="+alias+"&elementType="+type+"&limit=1&withInnerCollections=false")
    dict = json.loads(r.content)
    totalSize = dict['element']['collectionItems']['totalSize']

    '''Основной запрос, передаем totalSize в параметр limit для получения всего списка тайтлов'''
    r = requests.get("https://sa-web.okko.tv/screenapi/v1/noauth/collection/web/1?elementAlias="+alias+"&elementType="+type+"&limit="+str(totalSize)+"&withInnerCollections=false")
    print "https://sa-web.okko.tv/screenapi/v1/noauth/collection/web/1?elementAlias="+alias+"&elementType="+type+"&limit="+str(totalSize)+"&withInnerCollections=false"
    dict = json.loads(r.content)

    for element in dict['element']['collectionItems']['items']:

        film = {}

        age_rating = element['element']['ageAccessType']
        countries = get_countries(element['element']['countries'])

        try:
            duration = int(element['element']['duration'])/60000
        except:
            duration = ''

        genres = get_genres(element['element']['genres'])
        imdbRating = element['element']['imdbRating']
        kinopoiskRating = element['element']['kinopoiskRating']
        name = element['element']['name']
        originalName = element['element']['originalName']
        type = element['element']['type']
        #print element['element']['worldReleaseDate']

        try:
            worldReleaseDate = datetime.datetime.fromtimestamp(int(element['element']['worldReleaseDate'])/1000).strftime("%Y-%m-%d")
        except:
            worldReleaseDate = ''

        pay_types = parse_pay_type(element['element']['products'])


        film['age_rating'] = age_rating
        film['countries'] = countries
        film['duration'] = duration
        film['genres'] = genres
        film['imdbRating'] = imdbRating
        film['kinopoiskRating'] = kinopoiskRating
        film['name'] = name
        film['originalName'] = originalName
        film['type'] = type
        film['worldReleaseDate'] = worldReleaseDate
        film['pay_types'] = pay_types
        film['id'] = element['element']['id']
        film['alias'] = element['element']['alias']

        films.append(film)

        """
        print "age_rating: ", age_rating
        print "countries: ", ", ".join(countries)
        print "duration: ", duration
        print "genres: ", ", ".join(genres)
        print "imdbRating: ", imdbRating
        print "kinopoiskRating: ", kinopoiskRating
        print "name: ", name
        print "type: ", type
        print "worldReleaseDate: ", worldReleaseDate
        print "pay_types: ", pay_types
        print "\n"
        """

with io.open('okko_database.txt', 'w', encoding='utf8') as outfile:
    outfile.write(json.dumps(films, outfile, ensure_ascii=False))






