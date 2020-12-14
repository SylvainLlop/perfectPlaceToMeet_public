# coding: utf-8
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pp2m_project.settings")
django.setup()

import csv

from find_pp2m.models import City, Department


with open('./tools/all_cities.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        code_insee = str(row[0])
        try:
            latitude = float(row[5])
        except ValueError:
            latitude = 0
        try:
            longitude = float(row[6])
        except ValueError:
            longitude = 0

        if City.objects.filter(code_insee=code_insee).exists():
            city = City.objects.get(code_insee=code_insee)
            city.latitude = latitude
            city.longitude = longitude
            city.save()
