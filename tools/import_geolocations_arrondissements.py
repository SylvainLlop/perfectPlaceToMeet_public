# coding: utf-8

import django
django.setup()

import csv

from find_pp2m.models import City, Department

with open('eucircos_regions_departements_circonscriptions_communes_gps_addon.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        # Get data from city
        print(row)
        city_dept_num = row[4]
        city_name = row[8]
        if City.objects.filter(name=city_name, num_department=city_dept_num).exists():
            city = City.objects.get(name=city_name, num_department=city_dept_num)
            cp = row[9]
            lat = row[11]
            long = row[12]

            city.postal_code = cp[:5]
            try:
                city.latitude = float(lat)
                city.longitude = float(long)
                city.save()
            except ValueError:
                print('Problème avec {}'.format(city_name))



