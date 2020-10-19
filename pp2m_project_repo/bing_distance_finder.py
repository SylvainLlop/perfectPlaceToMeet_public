import os
import django

from urllib.request import urlopen
import zlib
import requests
import json

os.environ['DJANGO_SETTINGS_MODULE'] = 'pp2m_project.settings'
django.setup()

from find_pp2m.models import City, Journey


api_key = 'AIzaSyAYq-AcczCq1jWkM9g_v_KIY9S1sjmAkEg'

dep_cities = City.objects.filter(is_pref='True')
arr_cities = City.objects.filter(is_sous_pref='True')

icount = 0
nb = len(arr_cities)

for city_dep in dep_cities:
    icount += 1
    dep_name = city_dep.name
    dep_lon = city_dep.longitude
    dep_lat = city_dep.latitude
    print('Processing {}/{} : {}'.format(icount, nb, dep_name))

    for city_arr in arr_cities:
        arr_name = city_arr.name
        arr_lon = city_arr.longitude
        arr_lat = city_arr.latitude

        if not Journey.objects.filter(departure=dep_name, arrival=arr_name).exists():

            if Journey.objects.filter(departure=arr_name, arrival=dep_name).exists():
                journey_rvs = Journey.objects.get(departure=arr_name, arrival=dep_name)
                journey = Journey()
                journey.departure = dep_name
                journey.arrival = arr_name
                journey.distance = journey_rvs.distance
                journey.duration = journey_rvs.duration
                journey.save()

            # else:
            #     if arr_name != dep_name:
            #         base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='
            #         routeUrl = base_url + '{},{}&destinations={},{}'.format(dep_lat, dep_lon, arr_lat, arr_lon)
            #         routeUrl += '&key=' + api_key
#
            #         try:
            #             r = requests.get(routeUrl)
#
            #             x = r.json()
#
            #             distance = x['rows'][0]['elements'][0]['distance']['value']
            #             duration = x['rows'][0]['elements'][0]['duration']['value']
#
            #             journey = Journey()
            #             journey.departure = dep_name
            #             journey.arrival = arr_name
            #             journey.distance = distance
            #             journey.duration = duration
            #             journey.save()
#
            #         except:
            #             print('Problem with journey from {} to {}'.format(dep_name, arr_name))
#