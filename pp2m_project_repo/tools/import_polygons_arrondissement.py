# coding: utf-8
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pp2m_project.settings")
django.setup()

import json

from find_pp2m.models import City, Department

with open('arrondissements-version-simplifiee.geojson') as json_file:
    data_json = json.load(json_file)

    for feature in data_json["features"]:
        city_name = feature["properties"]["nom"]

        if City.objects.filter(name=city_name).exists():
            city = City.objects.get(name=city_name)
            if feature["geometry"]["type"] == 'Polygon':
                polygon_coordinates = feature["geometry"]["coordinates"][0]
            elif feature["geometry"]["type"] == 'MultiPolygon':
                # Take biggest polygon in multipolygon
                len_poly = 0
                for poly in feature["geometry"]["coordinates"]:
                    if len(poly[0]) > len_poly:
                        len_poly = len(poly[0])
                        polygon_coordinates = poly[0]

            # Remove last and redundant point
            polygon_coordinates = polygon_coordinates[:-1]

            # Reverse latitude and longitude
            polygon_coordinates = [[x,y] for [y,x] in polygon_coordinates]

            city.polygon = polygon_coordinates
            city.save()
