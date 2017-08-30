# -*- coding: utf-8 -*-

import glob, os
import json
import xlsxwriter


wb = xlsxwriter.Workbook('showjet_database.xlsx')
ws = wb.add_worksheet()

row = 1
ws.write(0, 0, u"Название")
ws.write(0, 1, u"Сезон\Коллекция")
ws.write(0, 2, u"Оригинальное название")
ws.write(0, 3, u"Онлайн-кинотеатр")
ws.write(0, 4, u"Бизнес-модель")
ws.write(0, 5, u"Год")


for file in glob.glob("*.txt"):
    #print file


    with open(file, 'r') as infile:
        films = json.loads(infile.read())
        for film in films:
            #pprint.pprint(film)

            ws.write(row, 0, film['title'])
            ws.write(row, 1, int(film['season']))
            ws.write(row, 2, film["original_title"])
            ws.write(row, 3, "showjet")
            ws.write(row, 4, film["business_type"])
            ws.write(row, 5, int(film["premiere_date_world"][:4]))
            row += 1


wb.close()