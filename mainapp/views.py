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
from django.core.mail import send_mail


Test_Merchant_ID = config('Test_Merchant_ID')
Test_Merchant_Key = config('Test_Merchant_Key')
User = get_user_model()
ELASTIC_URL = config('ELASTICSEARCH_URL')
es = Elasticsearch(ELASTIC_URL)


def error_404_view(request, exception):
    return render(request,'error_404.html')

def error_500_view(request):
    return render(request,'error_500.html')


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
    user_obj = User.objects.get(username = username)
    cart_obj = Cart.objects.filter(user__username = username)
        
    context = {
        "user_obj": user_obj,
        "cart_obj": cart_obj,
    }
    return render(request, 'profile.html', context)


def cart_items(request):
    username = request.user.username
    cart_obj = Cart.objects.filter(user__username = username)
    
    if request.method =="POST":
        head_count = request.POST.get("head_count")
        tour_date = request.POST.get("tour_date")
        cart_id = request.POST.get("cart_id")
        cart_title = request.POST.get("cart_title")
        print('------------------------',cart_id, cart_title)
        if cart_title != None:
            print('-------', 'paytm called')
            cart_id = request.POST.get("cart_id")
            cart = get_object_or_404(Cart, id = cart_id)
            cost = cart.tour.cost
            head_count = cart.head_count
            total_cost = cost*head_count
            context = {
                "cart":cart,
                "total_cost": total_cost
            }

            #request the PAYTM to transfer the amount after payment of user
            param_dict = {

                        'MID': Test_Merchant_ID,
                        'ORDER_ID': str(cart.id),
                        'TXN_AMOUNT': str(total_cost),
                        'CUST_ID': str(request.user.id),
                        'INDUSTRY_TYPE_ID': 'Retail',
                        'WEBSITE': 'WEBSTAGING',
                        'CHANNEL_ID': 'WEB',
                        'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest'
                        
            }
            checksum = Checksum.generate_checksum(param_dict, Test_Merchant_Key)
            
            return render(request, 'paytm.html', {'param_dict': param_dict, 'checksum':checksum})
        
        cart = get_object_or_404(Cart, id=cart_id)
        cart.tour_date = tour_date
        cart.head_count = head_count
        cart.save()  
        messages.success(request,'Items added to cart')
       
        return redirect("/cart-items/")
         
    context = {
        "cart_obj": cart_obj,
    }
    return render(request, 'cart_items.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user,)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    
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
        cart = Cart.objects.create(head_count = head_count, tour_date = tour_date, user=user, tour = tour)
        cart.save()  
        messages.success(request,'Items added to cart')
        tour = Tour.objects.get(id = tour_id)
        country_id = tour.country_id
        return redirect("/countries/"+str(country_id))
    return render(request, 'add_to_cart.html')
    # return redirect(reverse('checkout'))

@csrf_exempt
def handlerequest(request):
    Test_Merchant_Key = config('Test_Merchant_Key')
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, Test_Merchant_Key, checksum)
    
    if verify:
        if response_dict['RESPCODE'] == '01':
            order_id  = response_dict['ORDERID']
            cart = Cart.objects.get(id = order_id)
            cart.sell_status = True
            cart.save()  
            
            # user_obj = request.user
            # name = user_obj.first_name
            # email = user_obj.email
            
            # booking_detali = str(name)+"\n"+"order id" +str(order_id)+"\n" +"no of person" + str(cart.head_count)+ "tour date"+ str(cart.tour_date) + "tour"+ str(tour+ cart.tour.place)
            
            # send_mail("booking details", booking_detali,"paul@polo.com", [email])
            
            # print(request.user.email)
            # print(request.user.username)
            
            print("ok")
        else:
            print("not ok")
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

    
def booked_tours_detail(request,order_id ):
    cart_obj = get_object_or_404(Cart, id=order_id)
    total_cost = (cart_obj.tour.cost)*(cart_obj.head_count)
    context = {
        "cart_obj":cart_obj,
        "total_cost":total_cost 
    }
    return render(request, 'booked_tours_detail.html', context)
