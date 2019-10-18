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


def index(request):
    countries = Tour.objects.values('country').annotate(Count('country'))
    country_list = []
    for country in countries:
        country_list.append(country['country'])
        
    if request.method == 'POST':
        form = FindDestinationForm(request.POST)
        if form.is_valid():
            place = form.cleaned_data['place']
            print(place)
    form = FindDestinationForm()
    return render(request, 'index.html', {'form': form, 'countries': country_list})

def tour_select(request, name):
    form = FindDestinationForm()
    tours = Tour.objects.values().filter(country=name)
    return render(request, 'tourpage.html', {'tours': tours, 'country': name, 'form': form})


