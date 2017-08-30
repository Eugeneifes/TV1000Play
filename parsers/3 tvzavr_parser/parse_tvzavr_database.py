# -*- coding: utf-8 -*-
import io
import json
import xlsxwriter



with io.open('tvzavr_database.txt', 'r', encoding='utf8') as infile:
    database = json.loads(infile.read())


wb = xlsxwriter.Workbook('tvzavr_database.xlsx')
ws = wb.add_worksheet()
row = 1
memory = []


ws.write(0, 0, u"Название")
ws.write(0, 1, u"Сезон\Коллекция")
ws.write(0, 2, u"Оригинальное название")
ws.write(0, 3, u"Онлайн-кинотеатр")
ws.write(0, 4, u"Бизнес-модель")
ws.write(0, 5, u"Год")


for film in database:
    print film['id'], film['name']


    try:
        business_type = film['business_type']

        ws.write(row, 0, film['name'])
        ws.write(row, 1, "")
        ws.write(row, 2, "")
        ws.write(row, 3, "tvzavr")
        ws.write(row, 4, business_type)
        try:
            ws.write(row, 5, int(film['year']))
        except:
            ws.write(row, 5, '')

        row += 1

    except:
        for tariff in film['tariffs']:
            if tariff['type'] == 'est':
                business_type = "EST"
            elif tariff['type'] == 'subscription':
                business_type = "SVOD"
            elif tariff['type'] == 'purchase':
                business_type = "TVOD"


            if {"id": film["id"], "business_type": business_type} not in memory:

                memory.append({"id": film["id"], "business_type": business_type})

                ws.write(row, 0, film['name'])
                ws.write(row, 1, "")
                ws.write(row, 2, "")
                ws.write(row, 3, "tvzavr")
                ws.write(row, 4, business_type)
                try:
                    ws.write(row, 5, int(film['year']))
                except:
                    ws.write(row, 5, '')

                row += 1

wb.close()


