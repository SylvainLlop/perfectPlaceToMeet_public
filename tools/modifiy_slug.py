# coding: utf-8
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pp2m_project.settings")
django.setup()

import csv

from find_pp2m.models import City

all_cities = City.objects.all()

for city in all_cities:
    if ' ' in city.slug:
        city.slug = city.slug.replace(' ', '-')
        city.save()
