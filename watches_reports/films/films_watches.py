#-*- coding: utf-8 -*-

import requests
import csv
import datetime
import xlsxwriter
import json


def header(ws, start_date, end_date):

    data_col = 2

    ws.write(0, 0, "id")
    ws.write(0, 1, "name")

    while start_date < end_date:
        ws.write(0, data_col, start_date.strftime("%Y-%m-%d"))
        data_col += 1
        start_date += datetime.timedelta(days=1)


'''без Cookie webcaster не даст забирать информацию с морды'''
''''(Cookie время от времени необходимо обновлять)'''
'''когда Cookie протухает, функция request возвращает сообщение типа "Вам необходимо войти в систему или зарегистрироваться."'''

cookie = {"Cookie": "_ym_uid=1482740294880453806; serialNumber=8e99cc598fd415a981553f42ce2d9b7c; _ga=GA1.2.1895930662.1482740294; _gid=GA1.2.723201539.1503394642; _ym_isad=2; sidebar-open=1; _webcaster_new_session=BAh7CkkiD3Nlc3Npb25faWQGOgZFVEkiJTZmMWRlMjQzZmY5YmFkOTliMTU5N2FkOTEzYjliNzA5BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMSt6R1NuTlExUGlCaFZoemM0c3JPVmllMTFuRmdhbm44Tzlvb2pjaTFBYTA9BjsARkkiHXdhcmRlbi51c2VyLmN1c3RvbWVyLmtleQY7AFRbCEkiDUN1c3RvbWVyBjsARlsGaQOXNAZJIiIkMmEkMTAkQ0F5YmJOR2VnM2Z0b25OTHMzLkRUdQY7AFRJIiF3YXJkZW4udXNlci5jdXN0b21lci5zZXNzaW9uBjsAVHsGSSIUbGFzdF9yZXF1ZXN0X2F0BjsAVEl1OglUaW1lDc1eHcDUf0NZCToNbmFub19udW1pAZg6DW5hbm9fZGVuaQY6DXN1Ym1pY3JvIgcVIDoJem9uZUkiCFVUQwY7AFRJIhFwcmV2aW91c191cmwGOwBGSSICGQJodHRwOi8vd2ViY2FzdGVyLnByby9jbGllbnQvdHJhbnNhY3Rpb25zP2RhdGVfZnJvbT0yMDE3LTA0LTAxJmRhdGVfdG89MjAxNy0wOC0yMiZ0cmFuc2FjdGlvbiU1QmFjdGl2ZSU1RD0wJnRyYW5zYWN0aW9uJTVCYW1vdW50X2d0ZXElNUQ9JnRyYW5zYWN0aW9uJTVCYW1vdW50X2x0ZXElNUQ9JnRyYW5zYWN0aW9uJTVCY29kZSU1RD0mdHJhbnNhY3Rpb24lNUJjb21tZW50JTVEPVBMQVkmdHJhbnNhY3Rpb24lNUJjdXN0b21lciU1RD0mdHJhbnNhY3Rpb24lNUJldmVudCU1RD0mdHJhbnNhY3Rpb24lNUJoaWRlX3Rlc3RfdHJhbnNhY3Rpb25zJTVEPTAmdHJhbnNhY3Rpb24lNUJpZCU1RD0mdHJhbnNhY3Rpb24lNUJwYXJ0bmVyX2lkJTVEPSZ0cmFuc2FjdGlvbiU1QnBheW1lbnRfc2VydmljZSU1RD0mdHJhbnNhY3Rpb24lNUJwaG9uZSU1RD0mdHJhbnNhY3Rpb24lNUJwcm9tb19jb2RlJTVEPSZ0cmFuc2FjdGlvbiU1QnN0YXR1cyU1RD1maW5pc2gmdHJhbnNhY3Rpb24lNUJ0cmFuc2FjdGlvbl90eXBlcyU1RCU1QiU1RD0mdXRmOD0lRTIlOUMlOTMGOwBU--4ece06364185f25b447983c77002913c759168b3"}


'''Устанавливаем необходимый временной диапазон для отчета'''
start_date = datetime.datetime(2017, 8, 1)
end_date = datetime.datetime(2017, 9, 1)


'''Получаем список всех элементом, имеющихся на сервисе'''
r = requests.get("https://tv1000api.webcaster.pro/api/v4/viaplay/events.json")
data = json.loads(r.content)


'''По окончании работы программы будет создан файл films_watches.xlsx'''
wb = xlsxwriter.Workbook('films_watches.xlsx')
ws = wb.add_worksheet("Watches")

data_col = 2
data_row = 1


'''Основная часть скрипта'''
'''Идет перебор всех элементов на сервисе (из events.json), проверяются поля parent_id и children_count'''
'''Для сериалов одно из этих полей будет заполнено (у серий будет поле parent_id, у родительского элемента будет присутствовать children_count)'''
'''А вот для фильмов оба этих поля должны быть пустыми'''

header(ws, start_date, end_date)

for element in data:
    #print element
    if element['parent_id'] == None and element['children_count'] == None:
        print element["id"]

        print element["name"]
        ws.write(data_row, 0, int(element["id"]))
        ws.write(data_row, 1, element["name"])

        query = "https://webcaster.pro/client/charts/statistic_entries/event_views_count.csv?utf8=%E2%9C%93&chartable%5Binterval%5D=1.day&" \
            "q%5Bstart_gt_as_unixtime%5D=" + start_date.strftime("%Y-%m-%d") + \
            "&q%5Bstart_lt_as_unixtime%5D=" + end_date.strftime("%Y-%m-%d") + \
            "&q%5Bchannel_id_eq%5D=&q%5Brecord_id_eq%5D=" + str(element["id"]) + \
            "&q%5Bplatform_in%5D%5B%5D=" + "ios"\
            "&q%5Bplatform_in%5D%5B%5D=" + "android"\
            "&q%5Bplatform_in%5D%5B%5D=" + "smarttv"\
            "&q%5Bplatform_in%5D%5B%5D=" + "desktop"

        print query

        r = requests.get(query, cookies=cookie)

        with open("temp_database.txt", "w") as temp_file:
            temp_file.write(r.content)

        with open("temp_database.txt", "r") as temp_file:
            reader = csv.reader(temp_file, delimiter=";")
            next(reader)
            for row in reader:
                print row[0], row[1]

                ws.write(data_row, data_col, int(row[1]))
                data_col += 1
        data_row += 1
        data_col = 2
data_row = 1
data_col = 2

wb.close()




