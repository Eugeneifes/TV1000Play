# -*- coding: utf-8 -*-
import requests
import json
import datetime
import io
from bs4 import BeautifulSoup
import pprint

headers = {"Host": "api.showjet.ru",
                "Connection": "keep-alive",
                "X-SJ-TOKEN": "mqPcruIz9WWXBRiCeaJdo-_NL4hI19rhFGo2ZONuhcfH",
                "Origin": "https://showjet.ru",
                "X-SJ-DEVICE-MODEL": "Other/",
                "X-SJ-OS-NAME": "Windows 7",
                "X-SJ-OS-VERSION": "NuN",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
                "X-SJ-APP-VERSION": "2.0",
                "X-SJ-DEVICE-NAME": "Chrome/59.0",
                "Accept": "*/*",
                "X-SJ-DEVICE-TYPE": "browser_chrome",
                "Content-Type": "application/json",
                "Referer": "https://showjet.ru/serials",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4"}


def parse_genres(genres):
    genres_mass = []
    for genre in genres:
        genres_mass.append(genre['name'])
    return genres_mass


def parse_countries(countries):
    countries_mass = []
    for country in countries:
        countries_mass.append(country['name'])
    return countries_mass


def to_date(date):
    year = date["year"]
    day = date["day"]
    month = date["month"]
    return datetime.datetime(year, month, day).strftime("%Y-%m-%d")


'''Ќа данный момент количество единиц контента меньше 100, но со временем количество тайтлов может увеличитьс€'''
r = requests.get("https://api.showjet.ru/api/v2.1/serials.json?limit=100", headers=headers)
data = json.loads(r.content)
#pprint.pprint(data)

films = []

for element in data['data']['items']:
    print element['title']
    #pprint.pprint(element)


    for season in range(element['seasons_count']):
        film = {}

        film["season"] = str(season + 1)

        r = requests.get("https://showjet.ru/serials/" + str(element['id']) + "/season/" + str(season + 1))
        soup = BeautifulSoup(r.text)


        '''Ќеобходимо забирать информациб о цене единицы контента непосредственно со страницы, так как API не возвращает такую информацию'''
        if soup.find("span", class_="serial-palette__buy-now season-buy rentalBtn"):
            film["business_type"] = "EST"
            film["price"] = 99
            #price = soup.find("span", class_="serial-palette__buy-now season-buy rentalBtn").text
        else:
            film["business_type"] = "AVOD"
            film["price"] = ""


        film["id"] = element['id']
        film["title"] = element['title']
        film["original_title"] = element['original_title']

        film["premiere_date_sj"] = to_date(element['premiere_date_sj'])
        film["premiere_date_world"] = to_date(element['premiere_date_world'])

        try:
            film["premiere_date_rf"] = to_date(element['premiere_date_rf'])
        except:
            film["premiere_date_rf"] = ""

        film["rating_imdb"] = element['rating_imdb']

        try:
            film["rating_kinopoisk"] = element['rating_kinopoisk']
        except:
            film["rating_kinopoisk"] = ""

        film["age_rating"] = element['age_rating']
        film["genres"] = parse_genres(element['genres'])
        film["countries"] = parse_countries(element['countries'])
        film["sj_exclusive"] = element['sj_exclusive']
        film["type"] = element['type']

        films.append(film)


with io.open('showjet_database.txt', 'w', encoding='utf8') as outfile:
    outfile.write(json.dumps(films, outfile, ensure_ascii=False))
