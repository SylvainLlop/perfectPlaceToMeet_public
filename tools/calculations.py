import math
import numpy as np
import pandas as pd
from django.db.models import Q
from find_pp2m.models import City, Journey


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


def get_cities_weightings_old(departure_cities_dict, all_cities_list, method):
    depts_weightings_community = []
    depts_weightings_individual = []
    nb_cities = sum([int(city['nb_people']) for city in departure_cities_dict])

    # Get tuples with unique departure cities and their occurences in departure_cities_list
    departure_cities_tuples = [(x['city'], int(x['nb_people'])) for x in departure_cities_dict]

    for city in all_cities_list:
        city_weighting_individual = 0
        city_weighting_community = 0
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

                city_weighting_community += journey_weighting * dep_city_occurence
                if journey_weighting > city_weighting_individual:
                    city_weighting_individual = journey_weighting

        depts_weightings_community.append((city.num_department, city_weighting_community / nb_cities))
        depts_weightings_individual.append((city.num_department, city_weighting_individual))

    depts_weightings = {
        'com' : depts_weightings_community,
        'ind' : depts_weightings_individual
    }

    return depts_weightings


def get_cities_weightings_new(departure_cities_dict, method):
    nb_cities = sum([int(city['nb_people']) for city in departure_cities_dict])

    arr_cities_weightings = {}

    dep_cities_list = [x['city'].name for x in departure_cities_dict]

    db_method = method.replace('route_', '')
    columns_list = ['departure', 'arrival', db_method]
    dep_cities_df = pd.DataFrame.from_records(
        Journey.objects.filter(departure__in=dep_cities_list).values_list('departure', 'arrival', db_method), 
        columns=columns_list
    )

    com_df = pd.DataFrame(dep_cities_df.groupby('arrival').sum()[db_method])
    ind_df = pd.DataFrame(dep_cities_df.groupby('arrival').max()[db_method])

    com_df = com_df.sort_values(db_method)
    ind_df = ind_df.sort_values(db_method)

    arr_cities_list = list(dep_cities_df.arrival.unique())
    print(arr_cities_list)
    arr_cities_df = pd.DataFrame.from_records(
        City.objects.filter(Q(is_pref=True) | Q(is_sous_pref=True)).values_list('name', 'polygon'), 
        columns=['name', 'polygon']
    )

    com_df = pd.merge(com_df, arr_cities_df, left_on='arrival', right_on='name')

    print(com_df)
    print(ind_df)
    print(arr_cities_df)


    # for dep_city_tuple in departure_cities_tuples:
    #     dep_city = dep_city_tuple[0]
    #     dep_city_occurence = dep_city_tuple[1]
# 
    #     dep_city_journeys = Journey.objects.filter(departure=dep_city)
# 
    #     for dep_city_journey in dep_city_journeys:
    #         arr_city = dep_city_journey.arrival
    #         if method == 'raw_distance':
    #             journey_weighting = calculate_distance(dep_city, city)
    #         elif method == 'route_distance':
    #             journey_weighting = dep_city_journey.distance / 1000
    #         elif method == 'route_duration':
    #             journey_weighting = dep_city_journey.duration / 3600
# 
    #         if arr_cities in arr_cities_weightings_com:
    #             arr_cities_weightings_com[arr_cities] += journey_weighting
    #             if journey_weighting < arr_cities_weightings_in[arr_cities]:
    #                 arr_cities_weightings_in[arr_cities] = journey_weighting
    #         else:
    #             arr_cities_weightings_com[arr_cities] = journey_weighting
    #             arr_cities_weightings_in[arr_cities] = journey_weighting
# 
    # cities_weightings = {
    #     'com' : arr_cities_weightings_com,
    #     'ind' : arr_cities_weightings_in
    # }
# 
    # return cities_weightings


def calculate_mixed_criteria(entities, weightings):
    entities_weightings = {}
    std_wgs = {}

    for criteria in entities:
        entities_weightings[criteria] = zip(entities[criteria], weightings[criteria])
        entities_weightings[criteria] = sorted(entities_weightings[criteria], key=lambda weight: weight[0].name)
        std_wgs[criteria] = np.array([x[1] for x in entities_weightings[criteria]])
        std_wgs[criteria] = (std_wgs[criteria] - min(std_wgs[criteria])) / (max(std_wgs[criteria]) - min(std_wgs[criteria]))   
    
    entities_list = [x[0] for x in entities_weightings['com']]
    std_wgs['mix'] = np.array(std_wgs['com']) + np.array(std_wgs['ind'])
    std_wgs['mix'] = std_wgs['mix'] - min(std_wgs['mix']) + 1
    entities_weightings['mix'] = sorted(zip(entities_list, list(std_wgs['mix'])), key=lambda weight: weight[1])

    entities['mix'] = [x[0] for x in entities_weightings['mix']]
    weightings['mix'] = [x[1] for x in entities_weightings['mix']]

    return (entities, weightings)
