import math
from find_pp2m.models import Journey


def calculate_distance(city_A, city_B):
    # Calculate as the crow flies distance between two cities
    latA = math.radians(city_A.latitude)
    lonA = math.radians(city_A.longitude)
    latB = math.radians(city_B.latitude)
    lonB = math.radians(city_B.longitude)

    distance = math.acos(math.sin(latA) * math.sin(latB)
                         + math.cos(latA) * math.cos(latB) * math.cos(lonB - lonA)) * 6371

    distance = round(distance, 2)

    return distance


# def get_raw_distance_weighting(departure_cities_list, all_cities_list):
#     # Calculate weighting for as the crow flies distances
#     weightings = []
#     nb_cities = len(departure_cities_list)
#
#     for city in all_cities_list:
#         distance = 0
#         for dep_city in departure_cities_list:
#             distance += calculate_distance(dep_city[0], city)
#
#         weighting = distance / nb_cities
#
#         weightings.append(weighting)
#
#     return weightings
#
#
# def get_route_distance_weighting(departure_cities_list, all_cities_list):
#     # Calculate weighting for route distances
#     weightings = []
#     nb_cities = len(departure_cities_list)
#
#     for city in all_cities_list:
#         distance = 0
#         for dep_city in departure_cities_list:
#             if dep_city[0] != city:
#                 distance += Journey.objects.get(departure=dep_city[0].name, arrival=city.name).distance / 1000
#
#         weighting = distance / nb_cities
#
#         weightings.append(weighting)
#
#     return weightings


def get_cities_weightings(departure_cities_list, all_cities_list, method, criteria):
    depts_weightings = []
    nb_cities = len(departure_cities_list)

    for city in all_cities_list:
        city_weighting = 0
        for dep_city in departure_cities_list:
            if dep_city != city:
                journey_weighting = 0
                try:
                    if method == 'raw_distance':
                        journey_weighting = calculate_distance(dep_city, city)
                    elif method == 'route_distance':
                        journey_weighting = Journey.objects.get(departure=dep_city.name, arrival=city.name).distance / 1000
                    elif method == 'route_duration':
                        journey_weighting = Journey.objects.get(departure=dep_city.name, arrival=city.name).duration / 3600
                except:
                    print('Problème avec le trajet {} - {}'.format(dep_city.name, city.name))

                if criteria == 'community':
                    city_weighting += journey_weighting
                elif criteria == 'individual':
                    if journey_weighting > city_weighting:
                        city_weighting = journey_weighting

        if criteria == 'community':
            weighting = city_weighting / nb_cities
        elif criteria == 'individual':
            weighting = city_weighting

        depts_weightings.append((city.num_department, weighting))

    return depts_weightings
