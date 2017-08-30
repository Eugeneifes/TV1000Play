#-*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
import io
import json

catalog = requests.get("https://www.tvzavr.ru/api/tvz/catalog").text
root = ET.fromstring(catalog.encode('iso-8859-1'))

database = []

for elem in root:

    item = {}

    item['id'] = elem.attrib['id']
    item['name'] = elem.attrib['name']
    item['age_rating'] = elem.attrib['age-limit']
    item['duration'] = elem.attrib['duration']
    item['rating'] = elem.attrib['rating']
    item['views'] = elem.attrib['views']


    if elem.attrib['requires_subscription'] == "Yes":
        tariffs = []
        for tariff in elem.find("tariffs"):
            tariffs.append({"type": tariff.attrib['type-alias'], "price": tariff.attrib['price'], "duration": tariff.attrib['duration']})

        item['tariffs'] = tariffs
    else:
        item['business_type'] = "AVOD"


    countries = []
    genres = []
    directors = []

    for child in elem:

        if child.tag == 'category':
            item['category'] = child.attrib['title']

        if child.tag == 'director':
            directors.append(child.attrib['title'])

        if child.tag == 'country':
            countries.append(child.attrib['title'])

        if child.tag == 'year':
            item['year'] = child.attrib['title']

        if child.tag == 'genre':
            genres.append(child.attrib['title'])

    item['directors'] = directors
    item['countries'] = countries
    item['genres'] = genres

    database.append(item)

with io.open('tvzavr_database.txt', 'w', encoding='utf8') as outfile:
    outfile.write(json.dumps(database, outfile, ensure_ascii=False))
