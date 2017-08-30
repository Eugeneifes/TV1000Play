# -*- coding: utf-8 -*-
import io
import json
import xlsxwriter



with io.open('okko_database.txt', 'r', encoding='utf8') as infile:
    database = json.loads(infile.read())


wb = xlsxwriter.Workbook('okko_database.xlsx')
ws = wb.add_worksheet()

row = 1
memory = []

ws.write(0, 0, u"Название")
ws.write(0, 1, u"Сезон\Коллекция")
ws.write(0, 2, u"Оригинальное название")
ws.write(0, 3, u"Онлайн-кинотеатр")
ws.write(0, 4, u"Бизнес-модель")
ws.write(0, 5, u"Год")


"""
Бизнес-модели:
DTO=EST
RENT=TVOD
SUBSCRIPTION=SVOD
"""


for elem in database:

    if elem['pay_types'] != []:

        for pay_type in elem['pay_types']:
            if pay_type['business_type'] == 'DTO':
                business_type = "EST"
            elif pay_type['business_type'] == 'RENT':
                business_type = "TVOD"
            elif pay_type['business_type'] == 'SUBSCRIPTION':
                business_type = "SVOD"

            if {"id": elem['id'], "business_type": business_type} not in memory:
                memory.append({"id": elem['id'], "business_type": business_type})

                ws.write(row, 0, elem['name'])
                ws.write(row, 1, "")
                ws.write(row, 2, elem['originalName'])
                ws.write(row, 3, "tvzavr")
                ws.write(row, 4, business_type)

                try:
                    ws.write(row, 5, int(elem['worldReleaseDate'][:4]))
                except:
                    ws.write(row, 5, "")

                row += 1

    else:

        ws.write(row, 0, elem['name'])
        ws.write(row, 1, "")
        ws.write(row, 2, elem['originalName'])
        ws.write(row, 3, "tvzavr")
        ws.write(row, 4, "")
        try:
            ws.write(row, 5, int(elem['worldReleaseDate'][:4]))
        except:
            ws.write(row, 5, "")

        row += 1

wb.close()

