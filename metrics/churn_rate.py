#-*- coding: utf-8 -*-

import requests
import datetime
import csv
import StringIO
from bs4 import BeautifulSoup
import json
import calendar


"""грузим файл cookie"""
def load_cookie():
    with open("cookie.txt", "r") as cookie_file:
        cookie = cookie_file.read()
    return {"Cookie": cookie}


"""собираем базу за период (заново)"""
def get_database(start_date, end_date):
    r = requests.get(transactions_query + "&date_from=" + start_date.strftime("%Y-%m-%d") + "&date_to=" + end_date.strftime("%Y-%m-%d"), cookies=cookie)
    print (r.content)
    with open("transactions_database.txt", "w") as out_file:
        out_file.write(r.content)


"""обновляем базу"""
def update_database(start_date, end_date):
    r = requests.get(transactions_query + "&date_from=" + start_date.strftime("%Y-%m-%d") + "&date_to=" + end_date.strftime("%Y-%m-%d"), cookies=cookie)

    with open("temp_database.txt", "w") as temp_file:
        temp_file.write(r.content)

    with open("transactions_database.txt", "a") as out_file:
        with open("temp_database.txt", "r") as temp_file:
            for line in temp_file.readlines()[1:]:
                out_file.write(line)


"""получаем последнюю дату из базы(для обновления)"""
def get_last_date():
    with open("transactions_database.txt", "r") as in_file:
        reader = csv.reader(in_file, delimiter=';')
        list = []
        for row in reader:
            list.append(row)

        year = int(list[-1][1][:4])
        month = int(list[-1][1][5:7])
        day = int(list[-1][1][8:10])
        return datetime.date(year, month, day) + timedelta(days=1)


def get_total_subs(date):
    try:
        r = requests.get(all_subs_query + "&transaction%5Bstate_to_date%5D=" + date.strftime("%Y-%m-%d"), cookies=cookie)
        soup = BeautifulSoup(r.text)
        elem = soup.find("span", class_="pagination-extra")
        subscribers = elem.text.replace('(', '').replace(')', '').split('/')[1]
        return int(subscribers)
    except:
        return 0


"""получаем количество новых подписок за период"""
def get_new_subs(start_date, end_date):
    count_new_subs = 0

    with open("transactions_database.txt", "r") as in_file:
        reader = csv.reader(in_file, delimiter=";")
        next(reader)
        for row in reader:
            current_date = datetime.datetime.strptime(row[1][:10], '%Y-%m-%d')
            if current_date>=start_date and current_date<=end_date:
                if row[3].decode("cp1251").encode("utf-8").find(r'Покупка подписки') != -1 and row[3].decode("cp1251").encode("utf-8").find(r'Автоматическое продление') == -1:
                    count_new_subs += 1
    return count_new_subs


def get_last_date_month(month):
    year = int(month[:4])
    month_num = int(month[5:])
    return datetime.date(year, month_num, calendar.monthrange(year, month_num)[1])


def get_churn(start_date, end_date):

    dict = {}

    total_subs_start = get_total_subs(start_date)
    total_subs_end = get_total_subs(end_date)
    new_subs = get_new_subs(start_date=start_date, end_date=end_date)
    outflow = total_subs_start - total_subs_end + new_subs
    CR = float(outflow)/total_subs_end

    dict["new_subs"] = new_subs
    dict["total_subs_start"] = total_subs_start
    dict["total_subs_end"] = total_subs_end
    dict["outflow"] = outflow
    dict["CR"] = CR
    dict["month"] = start_date.strftime('%B') + start_date.strftime("%y")

    #print ("Новые подписчики: %d" % new_subs)
    #print ("Подписок на начало периода: %d" % total_subs_start)
    #print ("Подписок на конец периода: %d" % total_subs_end)
    #print ("Отток: %d" % (total_subs_start - total_subs_end + new_subs))

    print ("CR: %.2f" % CR)
    #print ("\n")
    return dict


def update_CR_file():

    january16 = get_churn(datetime.datetime(2016, 1, 1), datetime.datetime(2016, 1, 31))
    february16 = get_churn(datetime.datetime(2016, 2, 1), datetime.datetime(2016, 2, 29))
    march16 = get_churn(datetime.datetime(2016, 3, 1), datetime.datetime(2016, 3, 31))
    april16 = get_churn(datetime.datetime(2016, 4, 1), datetime.datetime(2016, 4, 30))
    may16 = get_churn(datetime.datetime(2016, 5, 1), datetime.datetime(2016, 5, 31))
    june16 = get_churn(datetime.datetime(2016, 6, 1), datetime.datetime(2016, 6, 30))
    july16 = get_churn(datetime.datetime(2016, 7, 1), datetime.datetime(2016, 7, 31))
    august16 = get_churn(datetime.datetime(2016, 8, 1), datetime.datetime(2016, 8, 31))
    september16 = get_churn(datetime.datetime(2016, 9, 1), datetime.datetime(2016, 9, 30))
    october16 = get_churn(datetime.datetime(2016, 10, 1), datetime.datetime(2016, 10, 31))
    november16 = get_churn(datetime.datetime(2016, 11, 1), datetime.datetime(2016, 11, 30))
    december16 = get_churn(datetime.datetime(2016, 12, 1), datetime.datetime(2016, 12, 31))
    january17 = get_churn(datetime.datetime(2017, 1, 1), datetime.datetime(2017, 1, 31))
    february17 = get_churn(datetime.datetime(2017, 2, 1), datetime.datetime(2017, 2, 28))
    march17 = get_churn(datetime.datetime(2017, 3, 1), datetime.datetime(2017, 3, 31))
    april17 = get_churn(datetime.datetime(2017, 4, 1), datetime.datetime(2017, 4, 30))

    print january16
    with open("CR_stats.txt", "w") as CR_stats:
        CR_stats.write(json.dumps([january16, february16, march16, april16, may16, june16, july16, august16, september16, october16, november16, december16, january17, february17, march17, april17]))


cookie = load_cookie()
all_subs_query = "https://webcaster.pro/admin/users?utf8=%E2%9C%93&q%5Bname_cont%5D=&q%5Bpartner_id_eq%5D=&transaction%5Btransaction_type_ids%5D%5B%5D=&transaction%5Btransaction_type_ids%5D%5B%5D=363&transaction%5Btransaction_type_ids%5D%5B%5D=371&transaction%5Btransaction_type_ids%5D%5B%5D=695&transaction%5Btransaction_type_ids%5D%5B%5D=383&transaction%5Btransaction_type_ids%5D%5B%5D=387&transaction%5Btransaction_type_ids%5D%5B%5D=375&transaction%5Btransaction_type_ids%5D%5B%5D=379&transaction%5Btransaction_type_ids%5D%5B%5D=205&transaction%5Btransaction_type_ids%5D%5B%5D=335&transaction%5Btransaction_type_ids%5D%5B%5D=331&transaction%5Btransaction_type_ids%5D%5B%5D=149&transaction%5Btransaction_type_ids%5D%5B%5D=299&transaction%5Btransaction_type_ids%5D%5B%5D=343&transaction%5Btransaction_type_ids%5D%5B%5D=193&transaction%5Bstate%5D=active&q%5Bcreated_at_gt%5D=&q%5Bcreated_at_lt%5D="
transactions_query = "https://webcaster.pro/client/transactions/export.csv?utf8=%E2%9C%93&transaction%5Bid%5D=&transaction%5Bcode%5D=&transaction%5Bevent%5D=&transaction%5Bcomment%5D=&transaction%5Btransaction_types%5D%5B%5D=&transaction%5Bcustomer%5D=&transaction%5Bphone%5D=&transaction%5Bhide_test_transactions%5D=0&transaction%5Bhide_test_transactions%5D=1&transaction%5Bactive%5D=0&transaction%5Bamount_gteq%5D=&transaction%5Bamount_lteq%5D=&transaction%5Bpartner_id%5D=&transaction%5Bpayment_service%5D=&transaction%5Bstatus%5D=finish&transaction%5Bpromo_code%5D="

#update_CR_file()

with open("CR_stats.txt", "r") as CR_stats:
    CR = json.loads(CR_stats.read())


with open("template.html", 'r') as template:
    with open("churn_rate.html", 'w') as churn_rate:
        html = template.read()
        churn_rate.write(html % tuple([rate['CR'] for rate in CR]))

