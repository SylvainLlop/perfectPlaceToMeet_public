# coding: utf-8

import django
django.setup()

import csv

from find_pp2m.models import City, Department

with open('import_ville_dept.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        # Get data from department
        num_dept = str(row[0])
        name_dept = row[1]
        pref = row[2]
        sous_prefs = row[3].split(',')

        # Record department
        dept = Department()
        dept.name = name_dept
        dept.num_department = num_dept
        dept.save()

        # Record prefecture
        cit = City()
        cit.name = pref
        cit.num_department = num_dept
        cit.is_pref = True
        cit.is_sous_pref = False
        cit.save()

        for sous_pref in sous_prefs:
            # Record sous-prefecture
            cit = City()
            cit.name = sous_pref
            cit.num_department = num_dept
            cit.is_pref = False
            cit.is_sous_pref = True
            cit.save()



