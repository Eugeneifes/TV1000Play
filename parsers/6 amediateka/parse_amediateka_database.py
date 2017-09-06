# -*- coding: utf-8 -*-
import glob, os
import io
import json
import csv
import xlsxwriter
import pprint
import requests


with io.open('amediateka_database.txt', 'r', encoding='utf8') as infile:
    films = json.loads(infile.read())

bundles_link = "https://api.amediateka.ru/v1/bundles.json?client_id=amediateka"
r = requests.get(bundles_link)
bundles_data = json.loads(r.content)



wb = xlsxwriter.Workbook('amediateka_titles.xlsx')
ws = wb.add_worksheet()

memory = []
row = 1
ws.write(0, 0, u"Название")
ws.write(0, 1, u"Сезон\Коллекция")
ws.write(0, 2, u"Оригинальное название")
ws.write(0, 3, u"Онлайн-кинотеатр")
ws.write(0, 4, u"Бизнес-модель")
ws.write(0, 5, u"Год")


for film in films:

    if film['object'] == 'serial':

        if film['bundles'] == []:
            #pprint.pprint(film)

            if {"id": film["serial_id"], "season": film['season_name'], "business_model": ""} not in memory:

                memory.append({"id": film["serial_id"], "season": film['season_name'], "business_model": ""})
                ws.write(row, 0, film['serial_name'])
                ws.write(row, 1, film['season_name'])
                ws.write(row, 2, film['serial_original_name'])
                ws.write(row, 3, "amediateka")
                ws.write(row, 4, "")
                ws.write(row, 5, int(film['year']))
                row += 1

        else:
            for bundle in film['bundles']:
                for element in bundles_data['bundles']:
                    if element['id'] == bundle['id']:
                        if element['object'] == 'tvod_bundle':
                            if {"id": film["serial_id"], "season": film['season_name'], "business_model": "TVOD"} not in memory:

                                memory.append({"id": film["serial_id"], "season": film['season_name'], "business_model": "TVOD"})
                                ws.write(row, 0, film['serial_name'])
                                ws.write(row, 1, film['season_name'])
                                ws.write(row, 2, film['serial_original_name'])
                                ws.write(row, 3, "amediateka")
                                ws.write(row, 4, "TVOD")
                                ws.write(row, 5, int(film['year']))
                                row += 1
                        else:
                            if {"id": film["serial_id"], "season": film['season_name'], "business_model": "SVOD"} not in memory:
                                memory.append({"id": film["serial_id"], "season": film['season_name'], "business_model": "SVOD"})

                                ws.write(row, 0, film['serial_name'])
                                ws.write(row, 1, film['season_name'])
                                ws.write(row, 2, film['serial_original_name'])
                                ws.write(row, 3, "amediateka")
                                ws.write(row, 4, "SVOD")
                                ws.write(row, 5, int(film['year']))
                                row += 1


    elif film['object'] == 'film':

        if film['bundles'] == []:
            #pprint.pprint(film)
            if {"id": film["slug"], "business_model": ""} not in memory:
                memory.append({"id": film["slug"], "business_model": ""})
                ws.write(row, 0, film['name'])
                ws.write(row, 1, "")
                ws.write(row, 2, film['original_name'])
                ws.write(row, 3, "amediateka")
                ws.write(row, 4, "")
                ws.write(row, 5, int(film['year']))
                row+=1

        else:
            for bundle in film['bundles']:
                for element in bundles_data['bundles']:
                    if element['id'] == bundle['id']:
                        if element['object'] == 'tvod_bundle':

                            if {"id": film["slug"], "business_model": "TVOD"} not in memory:
                                memory.append({"id": film["slug"], "business_model": "TVOD"})
                                ws.write(row, 0, film['name'])
                                ws.write(row, 1, "")
                                ws.write(row, 2, film['original_name'])
                                ws.write(row, 3, "amediateka")
                                ws.write(row, 4, "TVOD")
                                ws.write(row, 5, int(film['year']))
                                row += 1
                        else:

                            if {"id": film["slug"], "business_model": "SVOD"} not in memory:
                                memory.append({"id": film["slug"], "business_model": "SVOD"})
                                ws.write(row, 0, film['name'])
                                ws.write(row, 1, "")
                                ws.write(row, 2, film['original_name'])
                                ws.write(row, 3, "amediateka")
                                ws.write(row, 4, "SVOD")
                                ws.write(row, 5, int(film['year']))
                                row += 1



wb.close()




