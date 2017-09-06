import requests
import json
import io
import pprint

series_link = "https://api.amediateka.ru/v1/serials.json?client_id=amediateka&limit=1000"
films_link = "https://api.amediateka.ru/v1/films.json?client_id=amediateka&limit=1000"
bundles_link = "https://api.amediateka.ru/v1/bundles.json?client_id=amediateka"

links = [series_link, films_link]



def get_bundles(id):
    r = requests.get("https://api.amediateka.ru/v1/distributions.json?client_id=amediateka&ids="+id)
    data = json.loads(r.content)
    return data['distributions'][0]['bundles']


films = []

for link in links:
    r = requests.get(link)
    data = json.loads(r.content)

    if link == series_link:
        for element in data['serials']:

            r = requests.get("https://api.amediateka.ru/v1/serials/"+element['id']+"/seasons.json?client_id=amediateka")
            seasons = json.loads(r.content)

            for season in seasons['seasons']:
                #pprint.pprint(season)
                #print "\n"
                film = {}

                film['amediateka_rating'] = element['amediateka_rating']
                film['kinopoisk_rating'] = element['kinopoisk_rating']
                film['imdb_rating'] = element['imdb_rating']

                film['country'] = element['country']
                film['tvod'] = season['tvod']
                film['genres'] = ", ".join(element['genres'])
                film['serial_id'] = element['id']
                film['seson_id'] = season['id']

                film['slug'] = element['slug']


                film['soon'] = season['soon']
                film['available_start'] = season['available_start']

                film['number_of_seasons'] = element['number_of_seasons']
                film['season'] = season['number']

                film['serial_name'] = element['name']
                film['serial_original_name'] = element['original_name']
                film['season_name'] = season['name']

                film['year'] = season['year']

                film['restriction'] = element['restriction']
                film['original_broadcaster'] = element['original_broadcaster']

                film['kinopoisk_id'] = element['kinopoisk_id']
                film['imdb_id'] = element['imdb_id']
                film['object'] = element['object']

                film['free'] = season['free']
                film['free_episodes_count'] = element['free_episodes_count']
                film['new_episode_available'] = element['new_episode_available']
                film['new_season_available'] = element['new_season_available']
                film['premier'] = element['premier']

                try:
                    film['studios'] = element['studios'][0]['name']
                except:
                    film['studios'] = []


                film['bundles'] = get_bundles(season['id'])
                films.append(film)



    if link == films_link:
        for element in data['films']:

            film = {}

            film['amediateka_rating'] = element['amediateka_rating']
            film['kinopoisk_rating'] = element['kinopoisk_rating']
            film['imdb_rating'] = element['imdb_rating']

            film['country'] = element['country']
            film['tvod'] = element['tvod']
            film['genres'] = ", ".join(element['genres'])

            film['available_start'] = element['available_start']
            film['duration'] = element['duration']
            film['free'] = element['free']


            film['id'] = element['id']
            film['slug'] = element['slug']
            film['kinopoisk_id'] = element['kinopoisk_id']
            film['imdb_id'] = element['imdb_id']
            film['name'] = element['name']
            film['original_name'] = element['original_name']

            film['restriction'] = element['restriction']
            film['soon'] = element['soon']
            film['year'] = element['year']
            film['object'] = element['object']

            try:
                film['studios'] = element['studios'][0]['name']
            except:
                film['studios'] = []


            film['bundles'] = get_bundles(element['id'])
            #print film['bundles']
            films.append(film)


with io.open('amediateka_database.txt', 'w', encoding='utf8') as outfile:
    outfile.write(json.dumps(films, outfile, ensure_ascii=False))





