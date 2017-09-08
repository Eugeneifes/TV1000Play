#-*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from pymongo import MongoClient
import xlrd


conn = MongoClient('localhost', 27017)
watches = conn.GA.watches


def get_films():
    films = []
    rb = xlrd.open_workbook('bearing.xlsx')
    sheet = rb.sheet_by_index(0)
    for rownum in range(sheet.nrows-1):
        row = sheet.row_values(rownum+1)
        films.append([row[3], row[5]])
    return films

films = get_films()


def sortByDate(mass):
    return mass[0]

def sortByMon(mass):
    return mass["monday"]

def stacked_bar_chart():
    LG = []
    samsung = []
    Android = []
    iOS = []
    dates = []

    for film in films:
        print film[0]
        print watches.find({"name": film[0]}).count()
        for elem in watches.find({"name": film[0]}):

            dates.append(elem["date"])
            LG.append([elem["date"], elem["LG"]])
            samsung.append([elem["date"], elem["Samsung"]])
            Android.append([elem["date"], elem["Android"]])
            iOS.append([elem["date"], elem["iOS"]])


        samsung = sorted(samsung, key=sortByDate)
        LG = sorted(LG, key=sortByDate)
        iOS = sorted(iOS, key=sortByDate)
        Android = sorted(Android, key=sortByDate)
        dates = sorted(dates)


        iOS_bottom = [y[1] for y in samsung]
        LG_bottom = [x + y[1] for x, y in zip(iOS_bottom, iOS)]
        Android_bottom = [x + y[1] for x, y in zip(LG_bottom, LG)]

        samsung_chart = plt.bar([x for x in range(len(samsung))], [y[1] for y in samsung], width=1, color='r')
        iOS_chart = plt.bar([x for x in range(len(samsung))], [y[1] for y in iOS], width=1, color='y', bottom=iOS_bottom)
        LG_chart = plt.bar([x for x in range(len(samsung))], [y[1] for y in LG], width=1, color='b', bottom=LG_bottom)
        Android_chart = plt.bar([x for x in range(len(samsung))], [y[1] for y in Android], width=1, color='g', bottom=Android_bottom)

        plt.title(film[1])
        plt.xticks([x for x in range(len(samsung))], dates, rotation=30)
        plt.legend((samsung_chart[0], iOS_chart[0], LG_chart[0], Android_chart[0]), ('samsung', 'iOS', 'LG', 'Android'))
        plt.show()

        LG = []
        samsung = []
        Android = []
        iOS = []
        dates = []


def simple_bar_chart():
    LG = []
    samsung = []
    Android = []
    iOS = []
    dates = []

    for film in films:
        print film[0]
        print watches.find({"name": film[0]}).count()
        for elem in watches.find({"name": film[0]}):
            dates.append(elem["date"])
            LG.append([elem["date"], elem["LG"]])
            samsung.append([elem["date"], elem["Samsung"]])
            Android.append([elem["date"], elem["Android"]])
            iOS.append([elem["date"], elem["iOS"]])

        samsung = sorted(samsung, key=sortByDate)
        LG = sorted(LG, key=sortByDate)
        iOS = sorted(iOS, key=sortByDate)
        Android = sorted(Android, key=sortByDate)
        dates = sorted(dates)

        fig, ax = plt.subplots()

        print LG
        print samsung
        print iOS
        print dates

        samsung_chart = ax.bar([x for x in range(len(samsung))], [y[1] for y in samsung], width=0.1, color='r')
        iOS_chart = ax.bar([x+0.1 for x in range(len(samsung))], [y[1] for y in iOS], width=0.1, color='y')
        LG_chart = ax.bar([x+0.2 for x in range(len(samsung))], [y[1] for y in LG], width=0.1, color='b')
        Android_chart = ax.bar([x+0.3 for x in range(len(samsung))], [y[1] for y in Android], width=0.1, color='g')

        plt.title(film[1])
        plt.xticks([x for x in range(len(samsung))], dates, rotation=30)
        plt.legend((samsung_chart[0], iOS_chart[0], LG_chart[0], Android_chart[0]), ('samsung', 'iOS', 'LG', 'Android' ))
        plt.show()


        LG = []
        samsung = []
        Android = []
        iOS = []
        dates = []


def percentage_bar_chart():
    LG = []
    samsung = []
    Android = []
    iOS = []
    dates = []
    min = 100

    for film in films:
        print film[0]
        print watches.find({"name": film[0]}).count()
        for elem in watches.find({"name": film[0]}):

            dates.append(elem["date"])
            LG.append([elem["date"], elem["LG"]])
            samsung.append([elem["date"], elem["Samsung"]])
            Android.append([elem["date"], elem["Android"]])
            iOS.append([elem["date"], elem["iOS"]])



        samsung = sorted(samsung, key=sortByDate)
        LG = sorted(LG, key=sortByDate)
        iOS = sorted(iOS, key=sortByDate)
        Android = sorted(Android, key=sortByDate)
        dates = sorted(dates)


        samsung_percent_massive = []
        LG_percent_massive = []
        Android_percent_massive = []
        iOS_percent_massive =[]

        for i in range(len(samsung)):
            percent_samsung = 100*samsung[i][1]/(samsung[i][1]+LG[i][1]+Android[i][1]+iOS[i][1])
            percent_LG = 100*LG[i][1]/(samsung[i][1]+LG[i][1]+Android[i][1]+iOS[i][1])
            percent_Android = 100*Android[i][1]/(samsung[i][1]+LG[i][1]+Android[i][1]+iOS[i][1])
            percent_iOS = 100*iOS[i][1]/(samsung[i][1]+LG[i][1]+Android[i][1]+iOS[i][1])

            samsung_percent_massive.append(percent_samsung)
            LG_percent_massive.append(percent_LG)
            Android_percent_massive.append(percent_Android)
            iOS_percent_massive.append(percent_iOS)

        iOS_bottom = [y for y in samsung_percent_massive]
        LG_bottom = [x + y for x, y in zip(iOS_bottom, iOS_percent_massive)]
        Android_bottom = [x + y for x, y in zip(LG_bottom, LG_percent_massive)]

        samsung_chart = plt.bar([x for x in range(len(samsung))], [y for y in samsung_percent_massive], width=1, color='r')
        iOS_chart = plt.bar([x for x in range(len(samsung))], [y for y in iOS_percent_massive], width=1, color='y', bottom=iOS_bottom)
        LG_chart = plt.bar([x for x in range(len(samsung))], [y for y in LG_percent_massive], width=1, color='b', bottom=LG_bottom)
        Android_chart = plt.bar([x for x in range(len(samsung))], [y for y in Android_percent_massive], width=1, color='g', bottom=Android_bottom)


        plt.title(film[1])
        plt.xticks([x for x in range(len(samsung))], dates, rotation=30)
        plt.legend((samsung_chart[0], iOS_chart[0], LG_chart[0], Android_chart[0]), ('samsung', 'iOS', 'LG', 'Android'))
        plt.show()

        LG = []
        samsung = []
        Android = []
        iOS = []
        dates = []

def whatDay(day, month, year):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    a = (14 - month) // 12
    y = year - a
    m = month+12 * a-2
    result = ((7000 + (day + y + y//4 - y//100 + y//400 + (31*m) // 12)) % 7) - 1
    return days[result]


def parse_date(date):
    day = date[8:10]
    month = date[5:7]
    year = date[0:4]
    return day, month, year


def week_bar_chart():

    watch = []
    record = {}
    for film in films:
        for elem in watches.find({"name": film[0]}):
            day, month, year = parse_date(elem["date"])
            day_week = whatDay(int(day), int(month), int(year))
            record["day_week"] = day_week
            record["LG"] = elem["LG"]
            record["Samsung"] = elem["Samsung"]
            record["iOS"] = elem["iOS"]
            record["Android"] = elem["Android"]
            watch.append(record)
            record = {}

    total_mon = 0
    total_tue = 0
    total_wed = 0
    total_thu = 0
    total_fri = 0
    total_sat = 0
    total_sun = 0

    for elem in watch:

        if elem["day_week"] == "monday":
            total_mon += elem["LG"] + elem["Android"] + elem["iOS"] +elem["Samsung"]

        if elem["day_week"] == "tuesday":
            total_tue += elem["LG"] + elem["Android"] + elem["iOS"] +elem["Samsung"]

        if elem["day_week"] == "wednesday":
            total_wed += elem["LG"] + elem["Android"] + elem["iOS"] +elem["Samsung"]

        if elem["day_week"] == "thursday":
            total_thu += elem["LG"] + elem["Android"] + elem["iOS"] +elem["Samsung"]

        if elem["day_week"] == "friday":
            total_fri += elem["LG"] + elem["Android"] + elem["iOS"] +elem["Samsung"]

        if elem["day_week"] == "saturday":
            total_sat += elem["LG"] + elem["Android"] + elem["iOS"] +elem["Samsung"]

        if elem["day_week"] == "sunday":
            total_sun += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]


    week_days_label = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    watches_by_week_days = [total_mon, total_tue, total_wed, total_thu, total_fri, total_sat, total_sun]

    plt.title("weeks")
    plt.bar([x for x in range(len(watches_by_week_days))], watches_by_week_days, width=0.75)
    plt.xticks([x+0.4 for x in range(len(watches_by_week_days))], week_days_label, rotation=30)
    plt.show()


def watch_by_platform(platforms):

    watch = []
    record = {}
    for film in films:
        for elem in watches.find({"name": film[0]}):
            day, month, year = parse_date(elem["date"])
            day_week = whatDay(int(day), int(month), int(year))
            record["day_week"] = day_week
            record["LG"] = elem["LG"]
            record["Samsung"] = elem["Samsung"]
            record["iOS"] = elem["iOS"]
            record["Android"] = elem["Android"]
            watch.append(record)
            record = {}

    for platform in platforms:

        total_mon = 0
        total_tue = 0
        total_wed = 0
        total_thu = 0
        total_fri = 0
        total_sat = 0
        total_sun = 0

        for elem in watch:

            if elem["day_week"] == "monday":
                total_mon += elem[platform]

            if elem["day_week"] == "tuesday":
                total_tue += elem[platform]

            if elem["day_week"] == "wednesday":
                total_wed += elem[platform]

            if elem["day_week"] == "thursday":
                total_thu += elem[platform]

            if elem["day_week"] == "friday":
                total_fri += elem[platform]

            if elem["day_week"] == "saturday":
                total_sat += elem[platform]

            if elem["day_week"] == "sunday":
                total_sun += elem[platform]

        week_days_label = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        watches_by_week_days = [total_mon, total_tue, total_wed, total_thu, total_fri, total_sat, total_sun]

        plt.title("weeks - " + platform)
        plt.bar([x for x in range(len(watches_by_week_days))], watches_by_week_days, width=0.75)
        plt.xticks([x + 0.4 for x in range(len(watches_by_week_days))], week_days_label, rotation=30)
        plt.show()



def watch_by_film():
    for film in films:

        watch = []
        record = {}

        for elem in watches.find({"name": film[0]}):
            day, month, year = parse_date(elem["date"])
            day_week = whatDay(int(day), int(month), int(year))
            record["day_week"] = day_week
            record["LG"] = elem["LG"]
            record["Samsung"] = elem["Samsung"]
            record["iOS"] = elem["iOS"]
            record["Android"] = elem["Android"]
            watch.append(record)
            record = {}


        total_mon = 0
        total_tue = 0
        total_wed = 0
        total_thu = 0
        total_fri = 0
        total_sat = 0
        total_sun = 0

        for elem in watch:

            if elem["day_week"] == "monday":
                total_mon += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "tuesday":
                total_tue += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "wednesday":
                total_wed += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "thursday":
                total_thu += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "friday":
                total_fri += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "saturday":
                total_sat += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "sunday":
                total_sun += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

        week_days_label = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        watches_by_week_days = [total_mon, total_tue, total_wed, total_thu, total_fri, total_sat, total_sun]

        plt.title("weeks - " + film[1])
        plt.bar([x for x in range(len(watches_by_week_days))], watches_by_week_days, width=0.75)
        plt.xticks([x + 0.4 for x in range(len(watches_by_week_days))], week_days_label, rotation=30)
        plt.show()


def watch_by_day():

    watch_by_week = []

    for film in films:

        watch = []
        record = {}

        for elem in watches.find({"name": film[0]}):
            day, month, year = parse_date(elem["date"])
            day_week = whatDay(int(day), int(month), int(year))
            record["day_week"] = day_week
            record["LG"] = elem["LG"]
            record["Samsung"] = elem["Samsung"]
            record["iOS"] = elem["iOS"]
            record["Android"] = elem["Android"]
            watch.append(record)
            record = {}

        total_mon = 0
        total_tue = 0
        total_wed = 0
        total_thu = 0
        total_fri = 0
        total_sat = 0
        total_sun = 0

        new_record = {}
        for elem in watch:
            if elem["day_week"] == "monday":
                total_mon += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "tuesday":
                total_tue += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "wednesday":
                total_wed += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "thursday":
                total_thu += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "friday":
                total_fri += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "saturday":
                total_sat += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

            if elem["day_week"] == "sunday":
                total_sun += elem["LG"] + elem["Android"] + elem["iOS"] + elem["Samsung"]

        new_record["name"] = film[0]
        new_record["monday"] = total_mon
        new_record["tuesday"] = total_tue
        new_record["wednesday"] = total_wed
        new_record["thursday"] = total_thu
        new_record["friday"] = total_fri
        new_record["saturday"] = total_sat
        new_record["sunday"] = total_sun

        watch_by_week.append(new_record)

    print watch_by_week
    mon_mass = sorted(watch_by_week, key=lambda k: k['monday'], reverse=True)
    tue_mass = sorted(watch_by_week, key=lambda k: k['tuesday'], reverse=True)
    wed_mass = sorted(watch_by_week, key=lambda k: k['wednesday'], reverse=True)
    thu_mass = sorted(watch_by_week, key=lambda k: k['thursday'], reverse=True)
    fri_mass = sorted(watch_by_week, key=lambda k: k['friday'], reverse=True)
    sat_mass = sorted(watch_by_week, key=lambda k: k['saturday'], reverse=True)
    sun_mass = sorted(watch_by_week, key=lambda k: k['sunday'], reverse=True)

    for i in range(10):
        print mon_mass[i]["name"]

    print "\n"

    for i in range(10):
        print tue_mass[i]["name"]

    print "\n"

    for i in range(10):
        print wed_mass[i]["name"]

    print "\n"

    for i in range(10):
        print thu_mass[i]["name"]

    print "\n"

    for i in range(10):
        print fri_mass[i]["name"]

    print "\n"

    for i in range(10):
        print sat_mass[i]["name"]

    print "\n"

    for i in range(10):
        print sun_mass[i]["name"]


watch_by_film()