# -*- coding: utf-8 -*-

import urllib2
import requests
from bs4 import BeautifulSoup
import io
import json

'''Список ссылок, по которым можно получать контент'''
films_link = "http://megogo.net/ru/films"
series_link = "http://megogo.net/ru/series"
mult_link = "http://megogo.net/ru/mult"
show_link = "http://megogo.net/ru/show"


'''svod'''
subscribe_link1 = "http://megogo.net/ru/landing/mplus/popular"
subscribe_link2 = "http://megogo.net/ru/landing/mplus/editors-choice"
subscribe_link3 = "http://megogo.net/ru/landing/mplus/films"
subscribe_link4 = "http://megogo.net/ru/landing/mplus/series"
subscribe_link5 = "http://megogo.net/ru/landing/mplus/mult"
subscribe_link6 = "http://megogo.net/ru/landing/mplus/show"


'''tvod'''
tvod_link = "http://megogo.net/ru/premiere"



'''Подгружаем базу фильмов из файла, если парсер упал'''
def load_database():
    with io.open('megogo_avod_database.txt', 'r', encoding='utf8') as infile:
        films = json.loads(infile.read())
    return films


def get_ratings(ratings):
    kp_rating = None
    imdb_rating = None
    try:
        for elem in ratings.find_all("div", class_="externalRating-item"):
            if elem.find("span", class_="key").text == u'КиноПоиск':
                kp_rating = elem.find("strong", class_="value").text

            if elem.find("span", class_="key").text == 'IMDb':
                imdb_rating = elem.find("strong", class_="value").text
    except:
        pass

    print "kp_rating:", kp_rating
    print "imdb_rating:", imdb_rating
    return kp_rating, imdb_rating


def get_cast(team):
    cast_list = []
    try:
        actor_table = team.find("div", class_="infoi infoi_role")
        actors = actor_table.find_all("li")
        for actor in actors:
            cast_list.append(" ".join(actor.text.split()))
    except:
        pass

    print "cast:", ", ".join(cast_list)
    return cast_list


def get_directors(team):
    directors_list = []
    try:
        directors_table = team.find("div", class_="infoi infoi_director")
        directors = directors_table.find_all("li")
        for director in directors:
            directors_list.append(" ".join(director.text.split()))
    except:
        pass

    print "directors:", ", ".join(directors_list)
    return directors_list


def get_scriptwriters(team):
    scriptwriters_list = []
    try:
        scriptwriters_table = team.find("div", class_="infoi infoi_scenario")
        scriptwriters = scriptwriters_table.find_all("li")
        for scriptwriter in scriptwriters:
            scriptwriters_list.append(" ".join(scriptwriter.text.split()))
    except:
        pass

    print "scriptwriters:", ", ".join(scriptwriters_list)
    return scriptwriters_list

def get_producers(team):
    producers_list = []
    try:
        producers_table = team.find("div", class_="infoi infoi_producer")
        producers = producers_table.find_all("li")
        for producer in producers:
            producers_list.append(" ".join(producer.text.split()))
    except:
        pass

    print "producers:", ", ".join(producers_list)
    return producers_list



def get_names(soup):
    original_name = None
    film_name = " ".join(soup.find("h1", class_="view__title").text.split())

    try:
        original_name = " ".join(soup.find("h2", class_="view__title2").text.split())
    except:
        pass

    print "film_name:", film_name
    print "original_name:", original_name
    return film_name, original_name


def get_year(year):
    return year.a.text.split()[0]

def get_country(country):
    return country.a.text.split()[0]

def get_genre(genre):
    genres = []
    for elem in genre.find_all("a"):
        genres.append(elem.text)
    return genres

def get_time(time):
    return time.text.split()[0]

def get_age(age):
    return age.text.split()[0]

def get_quality(quality):
    return quality.text.split()[0]

def get_translation(translation):
    translation_list = []
    for elem in translation.text.split(","):
        translation_list.append(elem.split()[0])
    return translation_list

def get_subtitles(subtitles):
    subtitle_list = []
    for elem in subtitles.text.split(","):
        subtitle_list.append(elem.split()[0])
    return subtitle_list


def get_cost(page):
    cost = None
    try:
        cost = " ".join(page.find("a", class_="btn btn_color Overlay__btn").text.split())
    except:
        pass
    return cost



def get_info(info):

    year = None
    country = None
    genre = None
    time = None
    age = None
    quality = None
    translation = None
    subtitles = None

    content = info.find_all("div", class_="infoi__content")

    for i, elem in enumerate(info.find_all("h4")):

        if elem.text.split()[0] == u"Год:":
            year = get_year(content[i])

        if elem.text.split()[0] == u"Страна:":
            country = get_country(content[i])

        if elem.text.split()[0] == u"Жанр:":
            genre = get_genre(content[i])

        if elem.text.split()[0] == u"Время:":
            time = get_time(content[i])

        if elem.text.split()[0] == u"Возраст:":
            age = get_age(content[i])

        if elem.text.split()[0] == u"Качество:":
            quality = get_quality(content[i])

        if elem.text.split()[0] == u"Перевод:":
            translation = get_translation(content[i])

        if elem.text.split()[0] == u"Субтитры:":
            subtitles = get_subtitles(content[i])

    print "year:", year
    print "country:", country
    print "genre:", genre
    print "time:", time
    print "age:", age
    print "quality:", quality
    print "translation:", translation
    print "subtitles:", subtitles
    return year, country, genre, time, age, quality, translation, subtitles


def get_films(pagenum, position):

    page = requests.get(films_link + "/page_" + str(pagenum))
    soup = BeautifulSoup(page.text)

    for elem in soup.find_all("a", class_="voi__title-link"):

        film = {}

        id = elem['href'].split("/")[-1].split(".")[0]

        print "position:", position
        print "pagenum:", pagenum
        print "ID:", id

        if id not in ids:

            page = requests.get(elem['href'])
            soup = BeautifulSoup(page.text)

            ratings = soup.find("div", class_="info info_rating")
            kp_rating, imdb_rating = get_ratings(ratings)

            info = soup.find("div", class_="info info_summary")
            year, country, genre, time, age, quality, translation, subtitles = get_info(info)

            film_name, original_name = get_names(soup)
            cost = get_cost(soup)

            film["id"] = id
            film["original_name"] = original_name
            film["name"] = film_name
            film["kp_rating"] = kp_rating
            film["imdb_rating"] = imdb_rating
            film["year"] = year
            film["country"] = country
            film["genre"] = genre
            film["duration"] = time
            film["age"] = age
            film["quality"] = quality
            film["translation"] = translation
            film["subtitles"] = subtitles
            film["position"] = position
            film["pagenum"] = pagenum
            film["cost"] = cost
            film["business_model"] = "AVOD"
            film["content_type"] = "film"
            position += 1

            films.append(film)
            print "\n"

            with io.open('megogo_avod_database.txt', 'w', encoding='utf8') as outfile:
                outfile.write(json.dumps(films, outfile, ensure_ascii=False))

    return position, pagenum




films = []
pagenum = 35
position = 1701

films = load_database()

ids = []
for elem in films:
    ids.append(elem['id'])



while pagenum <= 85:

    position, pagenum = get_films(pagenum=pagenum, position=position)
    pagenum += 1

print films




