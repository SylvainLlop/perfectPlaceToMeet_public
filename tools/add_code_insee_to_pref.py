# coding: utf-8
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pp2m_project.settings")
django.setup()

import csv

from find_pp2m.models import City

all_cities = City.objects.all()

cities_dict = {}
with open('./tools/all_cities.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    next(csv_reader)
    for row in csv_reader:
        code_insee = row[0]
        city_name = row[2]
        cities_dict[city_name] = code_insee


for city in all_cities:
    if city.name in cities_dict:
        city.code_insee = cities_dict[city.name]
        city.save()
