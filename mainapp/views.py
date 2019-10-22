from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.conf import settings
from django.db.models import Count
from .forms import FindDestinationForm, UserForm, ProfileForm
from decouple import config
import os
from elasticsearch import Elasticsearch
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Tour, Cart, Profile, Country
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum


MERCHANT_KEY = "xxxxxxxxxx"
User = get_user_model()
ELASTIC_URL = config('ELASTICSEARCH_URL')
es = Elasticsearch(ELASTIC_URL)

def index(request):
    form = FindDestinationForm()
    countries = Country.objects.values()
    popular_tours = Tour.objects.values().filter(country__id=7)
        
    if request.method == 'POST':
        form = FindDestinationForm(request.POST)
        tours = Tour.objects.values()
        i = 1
        for tour in tours:
            es.index(index='tour', doc_type ='tour', id=i, body=tour)
            i += 1
        if form.is_valid():
            place = form.cleaned_data['place']
            search = es.search(index='tour', body={'query': {'multi_match': {'query': place, 'fields': ['*']}}})
            search_result = []
            for result in search['hits']['hits']:
                search_result.append(result['_source'])
        return render(request, 'index.html', {'form': form, 'countries': countries, 'search':search_result, 'popular_tours': popular_tours})
    return render(request, 'index.html', {'form': form, 'countries': countries, 'popular_tours': popular_tours})


def tour_packages(request, id):
    form = FindDestinationForm()
    tours = Tour.objects.filter(country__id=id)
    if tours:
        country = tours[0].country.name
    else:
        country = Country.objects.values('name').filter(id=id)[0]['name']

    if request.method == 'POST':
        form = FindDestinationForm(request.POST)
        i = 1
        packages = Tour.objects.values().filter(country=id)
        for package in packages:
            es.index(index=country.lower(), id=i, body=package)
            i += 1
        if form.is_valid():
            place = form.cleaned_data['place']
            search = es.search(index=country.lower(), body={'query': {'multi_match': {'query': place, 'fields': ['*']}}})
            search_result = []
            for result in search['hits']['hits']:   
                search_result.append(result['_source'])
        return render(request, 'tourpage.html', {'tours': tours, 'country': country, 'form': form, 'search':search_result})
    return render(request, 'tourpage.html', {'tours': tours, 'country':country, 'form': form})

@login_required
def profile(request):
    username = request.user.username
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    user_obj = User.objects.get(username = username)
    context = {
        "user_obj": user_obj,
        "user_form": user_form,
        "profile_form": profile_form
    }
    if request.method == 'POST':
        profile_update_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_update_form.is_valid() and profile_form.is_valid():
            profile_update_form.save()
            profile_form.save()
            return render(request, 'profile.html', context)
    return render(request, 'profile.html', context)

# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile or None)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return HttpResponseRedirect('/profile')

#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'update_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })
    
def select_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    context = {
        "tour":tour
    }
    return render(request, "add_to_cart.html", context)
    
@login_required
def add_to_cart(request, tour_id):
    if request.method =="POST":
        head_count = request.POST.get("head_count")
        tour_date = request.POST.get("tour_date")
        tour = get_object_or_404(Tour, id=tour_id)
        user = request.user
        cart = Cart.objects.create(head_count=head_count, tour_date=tour_date, user=user, tour=tour)
        cart.save()  
        messages.success(request,'Items added to cart')
        print(tour_date)
        return redirect("/checkout/"+str(cart.id))
        # return redirect("/tour_id/"+str(tour_id))

    return render(request, 'add_to_cart.html')
    # return redirect(reverse('checkout'))

@login_required
def checkout(request, cart_id):
    cart_id = int(cart_id)
    cart = Cart.objects.get(id = cart_id)
    cost = cart.tour.cost
    head_count = cart.head_count
    total_cost = cost*head_count
    context = {
        "cart":cart,
        "total_cost": total_cost,
    }
    if request.method=="POST":
        #request the PAYTM to transfer the amount after payment of user
        param_dict = {
            'MID': 'xyxyxyxyx',
            'ORDER_ID': str(cart.id),
            'TXN_AMOUNT': str(total_cost),
            'CUST_ID': request.user.email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'DEFAULT',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})
    return render(request, 'checkout.html', context)


#handles the paytm post request
@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
