# -*- coding: utf-8 -*-

import glob
import json
import xlsxwriter


wb = xlsxwriter.Workbook('megogo_database.xlsx')
ws = wb.add_worksheet()

row = 1

ws.write(0, 0, u"Название")
ws.write(0, 1, u"Сезон\Коллекция")
ws.write(0, 2, u"Оригинальное название")
ws.write(0, 3, u"Онлайн-кинотеатр")
ws.write(0, 4, u"Бизнес-модель")
ws.write(0, 5, u"Год")


for file in glob.glob("*.txt"):
    print file


    with open(file, 'r') as infile:
        films = json.loads(infile.read())
        for film in films:

            #print film['name'].encode('iso-8859-1')
            try:
                ws.write(row, 0, film['name'])
            except:
                ws.write(row, 0, "")

            ws.write(row, 1, "")
            ws.write(row, 2, film['original_name'])
            ws.write(row, 3, "megogo")
            ws.write(row, 4, film['business_model'])
            ws.write(row, 5, film['year'])

            row += 1

wb.close()




"""
    if file in ['megogo_films_database.txt', 'megogo_mult_database.txt', 'megogo_series_database.txt', 'megogo_show_database.txt']:
        with io.open(file, 'r', encoding='utf8') as infile:
            films = json.loads(infile.read())
            for film in films:
                count+=1

    elif file == 'megogo_svod_database.txt':
    elif file == 'megogo_svod_database.txt':
    """

