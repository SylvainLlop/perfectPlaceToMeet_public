import json
from django.shortcuts import HttpResponse, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core import serializers
from django.db.models import Q

from django.views.generic import TemplateView
from django.forms import formset_factory

from .models import City, Department
from .forms import ParamForm, JourneyForm
from tools.calculations import *
from itertools import chain
from dal import autocomplete

import re


def index(request):
    response = 'Hello, world'
    return HttpResponse(response)


def pp2m_search(request, dep_cities_dict, method, criteria):
    keep_top = 10

    # Calculate weight for each department
    all_prefs = City.objects.filter(is_pref='True')
    depts_weightings = get_cities_weightings(dep_cities_dict, all_prefs, method, criteria)

    # Separate top and bottom weights
    depts_weightings = sorted(depts_weightings, key=lambda weight: weight[1])
    top_depts_weightings = depts_weightings[:keep_top]
    bot_depts_weightings = depts_weightings[keep_top:]

    # Get departments from bottom weights (both ordered by num_dept as it is the default for Department model)
    bot_depts_weightings = sorted(bot_depts_weightings, key=lambda weight: weight[0])
    bot_depts_list = [x[0] for x in bot_depts_weightings]
    bottom_depts = Department.objects.filter(num_department__in=bot_depts_list)

    # Get cities from top department weights
    top_depts_list = [x[0] for x in top_depts_weightings]
    top_cities = City.objects.filter(num_department__in=top_depts_list).filter(Q(is_pref=True) | Q(is_sous_pref=True))
    top_cities_weightings = get_cities_weightings(dep_cities_dict, top_cities, method, criteria)

    # Isolate weightings from results
    bot_depts_weightings_values = [x[1] for x in bot_depts_weightings]
    top_cities_weightings_values = [x[1] for x in top_cities_weightings]

    # Combine entities and sort by weightings
    entities_combined = list(chain(top_cities, bottom_depts))
    weightings = top_cities_weightings_values + bot_depts_weightings_values
    weightings, entities_combined = (list(t) for t in zip(*sorted(zip(weightings, entities_combined), key=lambda x: x[0])))

    # Convert in JSON
    dep_cities_list = [x['city'] for x in dep_cities_dict]
    dep_cities_nbpeople = [x['nb_people'] for x in dep_cities_dict]
    all_entities_json = serializers.serialize('json', entities_combined, fields=('name', 'polygon'))
    weightings_json = json.dumps(weightings)
    cities_json = serializers.serialize('json', dep_cities_list, fields=('name', 'latitude', 'longitude'))
    nbpeople_json = json.dumps(dep_cities_nbpeople)
    method_json = json.dumps(method)

    return render(request, 'find_pp2m/pp2m_distance.html', {
        'initial_cities': cities_json,
        'method': method_json,
        'all_entities': all_entities_json,
        'weightings': weightings_json,
        'nb_people': nbpeople_json,
    })


def pp2m_form(request):
    JourneyFormSet = formset_factory(JourneyForm, extra=3, can_delete=True)
    if request.method == 'POST':
        formset = JourneyFormSet(request.POST, request.FILES)
        paramForm = ParamForm(request.POST)

        if formset.is_valid() and paramForm.is_valid():
            cities_dict = [form.cleaned_data for form in formset if len(form.cleaned_data) > 0]

            method = paramForm.cleaned_data['method']
            criteria = paramForm.cleaned_data['criteria']

            return pp2m_search(request, cities_dict, method, criteria)


    else:
        formset = JourneyFormSet()
        paramForm = ParamForm()
    return render(request, 'find_pp2m/pp2m_formset.html', {'journey_formset': formset, 'param_form': paramForm})


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated:
        #     return City.objects.none()

        qs = City.objects.all()

        if self.q:
            self.q = re.sub('[aàâäAÀÁÂÃÄÅÆ]', 'a', self.q)
            self.q = re.sub('[cçC]', 'c', self.q)
            self.q = re.sub('[eéèêëEÉÈÊË]', 'e', self.q)
            self.q = re.sub('[iïîIÌÍÎÏ]', 'i', self.q)
            self.q = re.sub('[oôöÒÓÔÕÖ]', 'o', self.q)
            self.q = re.sub('[uüûùUÜÛÙÚ]', 'u', self.q)
            self.q = re.sub('[yYÿÝ]', 'y', self.q)
            self.q = self.q.lower()
            qs = qs.filter(slug__istartswith=self.q)

        return qs