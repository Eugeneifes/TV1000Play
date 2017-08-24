# -*- coding: utf-8 -*-

import glob
import json
import xlsxwriter

wb = xlsxwriter.Workbook('ivi_database.xlsx')
ws = wb.add_worksheet()
row = 1
memory = []



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
            print film['title']

            if film['business_type']:
                if film['object_type'] == 'video':

                    ws.write(row, 0, film['title'])
                    ws.write(row, 1, "")
                    ws.write(row, 2, film['orig_title'])
                    ws.write(row, 3, "ivi")
                    ws.write(row, 4, film['business_type'])
                    ws.write(row, 5, film['year'])

                    row += 1

                else:
                    if film['season']:
                        ws.write(row, 0, film['compilation_title'])
                        ws.write(row, 1, film['season'])
                        ws.write(row, 2, "")
                        ws.write(row, 3, "ivi")
                        ws.write(row, 4, film['business_type'])
                        ws.write(row, 5, film['year'])
                        row += 1
                    else:
                        ws.write(row, 0, film['compilation_title'])
                        ws.write(row, 1, film['compilation_name'])
                        ws.write(row, 2, "")
                        ws.write(row, 3, "ivi")
                        ws.write(row, 4, film['business_type'])
                        ws.write(row, 5, film['year'])
                        row += 1

            else:
                for content_paid_type in film['content_paid_types']:
                    if {"id": film["id"], "business_type": content_paid_type['ownership_type']} not in memory:
                        memory.append({"id": film["id"], "business_type": content_paid_type['ownership_type']})

                        if film['object_type'] == 'video':

                            ws.write(row, 0, film['title'])
                            ws.write(row, 1, "")
                            ws.write(row, 2, film['orig_title'])
                            ws.write(row, 3, "ivi")
                            ws.write(row, 4, content_paid_type['ownership_type'])
                            ws.write(row, 5, film['year'])

                            row += 1

                        else:
                            if film['season']:
                                ws.write(row, 0, film['compilation_title'])
                                ws.write(row, 1, film['season'])
                                ws.write(row, 2, "")
                                ws.write(row, 3, "ivi")
                                ws.write(row, 4, content_paid_type['ownership_type'])
                                ws.write(row, 5, film['year'])
                                row += 1
                            else:
                                ws.write(row, 0, film['compilation_title'])
                                ws.write(row, 1, film['compilation_name'])
                                ws.write(row, 2, "")
                                ws.write(row, 3, "ivi")
                                ws.write(row, 4, content_paid_type['ownership_type'])
                                ws.write(row, 5, film['year'])
                                row += 1

wb.close()