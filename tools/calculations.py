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


def get_cities_weightings(departure_cities_dict, all_cities_list, method, criteria):
    depts_weightings = []
    nb_cities = sum([int(city['nb_people']) for city in departure_cities_dict])

    # Get tuples with unique departure cities and their occurences in departure_cities_list
    departure_cities_tuples = [(x['city'], int(x['nb_people'])) for x in departure_cities_dict]

    for city in all_cities_list:
        city_weighting = 0
        for dep_city_tuple in departure_cities_tuples:
            dep_city = dep_city_tuple[0]
            dep_city_occurence = dep_city_tuple[1]
            if dep_city != city:
                journey_weighting = 0
                try:
                    if method == 'raw_distance':
                        journey_weighting = calculate_distance(dep_city, city)
                    elif method == 'route_distance':
                        journey_weighting = Journey.objects.get(departure=dep_city.pref_name, arrival=city.name).distance / 1000
                    elif method == 'route_duration':
                        journey_weighting = Journey.objects.get(departure=dep_city.pref_name, arrival=city.name).duration / 3600
                except:
                    print('Problème avec le trajet {} - {}'.format(dep_city.pref_name, city.name))

                if criteria == 'community':
                    city_weighting += journey_weighting * dep_city_occurence
                elif criteria == 'individual':
                    if journey_weighting > city_weighting:
                        city_weighting = journey_weighting

        if criteria == 'community':
            weighting = city_weighting / nb_cities
        elif criteria == 'individual':
            weighting = city_weighting

        depts_weightings.append((city.num_department, weighting))

    return depts_weightings
