# coding: utf-8
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pp2m_project.settings")
django.setup()

import csv

from find_pp2m.models import City, Department

arrs_dict = {}

# Create dictionary with pref and sous-pref
with open('./tools/comsimp2018.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    line_count = 0
    next(csv_reader)
    for row in csv_reader:
        if row[10] == '':
            city_name = row[11]
        else:
            city_name = row[10].replace('(','').replace(')','') + ' ' + row[11]
        dept_num = row[3]
        arr_num = row[5]

        if len(dept_num) == 2 and dept_num not in ['2A', '2B']: 
            # Add dept to dict
            if dept_num not in arrs_dict:
                arrs_dict[dept_num] = {}
            
            # Add arr to dept in dict
            if arr_num not in arrs_dict[dept_num].keys():
                arrs_dict[dept_num][arr_num] = ''
     
            # Add pref if exists in model
            if City.objects.filter(name=city_name, num_department=dept_num).exists():
                arrs_dict[dept_num][arr_num] = city_name

for dept_num in arrs_dict:
    for arr_num in arrs_dict[dept_num]:
        if arrs_dict[dept_num][arr_num] == '':
            cities_from_db = City.objects.filter(num_department=dept_num)
            
            cities_from_dict = arrs_dict[dept_num]
            cities_from_dict = list(cities_from_dict.values())

            for city in cities_from_db:
                if city.name not in cities_from_dict:
                    arrs_dict[dept_num][arr_num] = city.name


# Import cities from comsimp
cities_dict = {}
with open('./tools/comsimp2018.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    line_count = 0
    next(csv_reader)
    for row in csv_reader:
        if row[10] == '':
            city_name = row[11]
        else:
            city_name = row[10].replace('(','').replace(')','') + ' ' + row[11]
        dept_num = row[3]
        code_insee = row[3] + row[4]
        arr_num = row[5]

        if len(dept_num) == 2 and dept_num not in ['2A', '2B']: 
            cities_dict[code_insee] = {
                'comsimp_name' : city_name,
                'pref_related' : arrs_dict[dept_num][arr_num]
            }

# Import cities from eurocircos
with open('./tools/eucircos_regions_departements_circonscriptions_communes_gps.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    next(csv_reader)
    for row in csv_reader:
        code_insee = row[10]
        code_postal = row[9]
        city_name = row[8]
        latitude = row[11]
        longitude = row[12]
        dept_num = row[4]

        if len(dept_num) == 2 and dept_num not in ['2A', '2B']:   
            if code_insee in cities_dict:
                cities_dict[code_insee]['eurocircos_name'] = city_name
                cities_dict[code_insee]['latitude'] = latitude
                cities_dict[code_insee]['longitude'] = longitude
                cities_dict[code_insee]['code_postal'] = code_postal
            else:
                cities_dict[code_insee] = {
                    'eurocircos_name' : city_name,
                    'latitude' : latitude,
                    'longitude' : longitude,
                    'code_postal' : code_postal
                }

# Erase cities with missing data
code_insee_to_remove =[]
for code_insee in cities_dict:
    try:
        eurocircos = cities_dict[code_insee]['eurocircos_name']
        comsimp_name_test = cities_dict[code_insee]['comsimp_name']
    except KeyError:
        code_insee_to_remove.append(code_insee)

for code_insee in code_insee_to_remove:
    del cities_dict[code_insee]

# Write CSV
file_new_cities = './tools/all_cities.csv'
with open(file_new_cities, "w", newline='', encoding='utf-8') as csvfile:
    ordered_fieldnames = [
        'code_insee',
        'code_postal',
        'eurocircos_name',
        'comsimp_name',
        'pref_related',
        'latitude',
        'longitude'
        ]
    writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=ordered_fieldnames)
    writer.writeheader()

    for code_insee in cities_dict.keys():
        try:
            writer.writerow({'code_insee': code_insee, 
                            'code_postal': str(cities_dict[code_insee]['code_postal']), 
                            'eurocircos_name': str(cities_dict[code_insee]['eurocircos_name']), 
                            'comsimp_name': str(cities_dict[code_insee]['comsimp_name']), 
                            'pref_related': str(cities_dict[code_insee]['pref_related']),
                            'latitude': str(cities_dict[code_insee]['latitude']), 
                            'longitude': str(cities_dict[code_insee]['longitude'])
                            })
        except Exception as ex:
            if ex.args[0] == 'eurocircos_name':
                print('Not in eurocircos: {} ({})'.format(cities_dict[code_insee]['comsimp_name'], code_insee))
            if ex.args[0] == 'comsimp_name':
                print('Not in comsimp: {} ({})'.format(cities_dict[code_insee]['eurocircos_name'], code_insee))
csvfile.close()

