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
        code_postal = str(row[1])
        city_name = row[3]
        dept_num = str(row[0])[:2]
        pref_name = row[4]
        try:
            latitude = float(row[5])
        except ValueError:
            latitude = 0
        try:
            longitude = float(row[6])
        except ValueError:
            longitude = 0

        if not City.objects.filter(code_insee=code_insee).exists():
            if longitude != 0 and latitude != 0:
                cit = City()
                cit.name = city_name
                cit.num_department = dept_num
                cit.postal_code = code_postal
                cit.code_insee = code_insee
                cit.pref_name = pref_name
                cit.is_pref = False
                cit.is_sous_pref = False
                cit.save()
