from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from .forms import FindDestinationForm
from .models import Tour, Profile
from decouple import config
import os
from elasticsearch import Elasticsearch

ELASTIC_URL = config('ELASTICSEARCH_URL')
es = Elasticsearch(ELASTIC_URL)

# def search(request, country=None):
#     if country is not None:
#         i = 1
#         packages = Tour.objects.values().filter(country=country)
#         for package in packages:
#             es.index(index=country, id=i, body=package)
#             i += 1
#         return

#     tours = Tour.objects.values('title', 'country', 'id')
#     i = 1
#     for tour in tours:
#         es.index(index='tour', doc_type ="tour", id=i, body=tour)
#         i += 1

def index(request):
    form = FindDestinationForm()
    countries = Tour.objects.values('country').annotate(Count('country'))
    country_list = []
    for country in countries:
        country_list.append(country['country'])
        
    if request.method == 'POST':
        form = FindDestinationForm(request.POST)
        tours = Tour.objects.values('title', 'country', 'id')
        i = 1
        for tour in tours:
            es.index(index='tour', doc_type ="tour", id=i, body=tour)
            i += 1
        if form.is_valid():
            place = form.cleaned_data['place']
            search = es.search(index='tour', body={'query': {'multi_match': {'query': place, 'fields': ['*']}}})
            search_result = []
            for result in search['hits']['hits']:
                search_result.append(result['_source'])
        return render(request, 'index.html', {'form': form, 'countries': country_list, 'search':search_result})
    return render(request, 'index.html', {'form': form, 'countries': country_list})


def tour_select(request, name):
    form = FindDestinationForm()
    tours = Tour.objects.values().filter(country=name)

    if request.method == 'POST':
        form = FindDestinationForm(request.POST)
        i = 1
        packages = Tour.objects.values().filter(country=name)
        for package in packages:
            es.index(index=name.lower(), id=i, body=package)
            i += 1
       
        if form.is_valid():
            place = form.cleaned_data['place']
            search = es.search(index=name.lower(), body={'query': {'multi_match': {'query': place, 'fields': ['*']}}})
            search_result = []
            for result in search['hits']['hits']:   
                search_result.append(result['_source'])
        return render(request, 'tourpage.html', {'tours': tours, 'country': name, 'form': form, 'search':search_result})

    return render(request, 'tourpage.html', {'tours': tours, 'country': name, 'form': form})


