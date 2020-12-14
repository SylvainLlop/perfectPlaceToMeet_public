# coding: utf-8
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pp2m_project.settings")
django.setup()

import re

import csv

from find_pp2m.models import City

all_cities = City.objects.all()

for city in all_cities:
    city_slug = city.name
    city_slug = re.sub('[aàâäAÀÁÂÃÄÅÆ]', 'a', city_slug)
    city_slug = re.sub('[cçC]', 'c', city_slug)
    city_slug = re.sub('[eéèêëEÉÈÊË]', 'e', city_slug)
    city_slug = re.sub('[iïîIÌÍÎÏ]', 'i', city_slug)
    city_slug = re.sub('[oôöÒÓÔÕÖ]', 'o', city_slug)
    city_slug = re.sub('[uüûùUÜÛÙÚ]', 'u', city_slug)
    city_slug = re.sub('[yYÿÝ]', 'y', city_slug)
    city_slug = re.sub('[æ]', 'ae', city_slug)
    city_slug = re.sub('[œ]', 'oe', city_slug)
    city_slug = city_slug.lower()
    city.slug = city_slug
    city.save()


