from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from .forms import UserForm, ProfileForm
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from .forms import FindDestinationForm
from .models import Tour, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Tour, Cart
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
MERCHANT_KEY = "xxxxxxxxxx"



User = get_user_model()


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
    return render(request, 'index.html', {'form': form})

@login_required
def profile(request):
    username = request.user.username
    
    user_obj = User.objects.get(username = username)
    cart_obj = Cart.objects.filter(user__username = username)
    
    for i in cart_obj:
        print(i.id)
    
        
        
    context = {
        "user_obj": user_obj,
        "cart_obj": cart_obj,
    }
    return render(request, 'profile.html', context)

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
    
def add_to_cart(request, tour_id):
    print("abhishek")
    if request.method =="POST":
        head_count = request.POST.get("head_count")
        tour_date = request.POST.get("tour_date")
        tour = get_object_or_404(Tour, id=tour_id)
        print(tour)
        user = request.user
        print("user", user)
        print("tour", tour)
        print("head", head_count)
        print("tour_date", tour_date)
        cart = Cart.objects.create(head_count = head_count, tour_date = tour_date, user=request.user, tour = tour)
        cart.save()  
        messages.success(request,'Items added to cart')
        return redirect("/checkout/"+str(cart.id))
        print("user", user)
    return render(request, 'add_to_cart.html')
    # return redirect(reverse('checkout'))


def checkout(request, cart_id):
    cart_id = int(cart_id)
    cart = Cart.objects.get(id = cart_id)
    cost = cart.tour.cost
    head_count = cart.head_count
    total_cost = cost*head_count
    context = {
        "cart":cart,
        "total_cost": total_cost
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


def booked_tours_detail(request,order_id ):
    cart_obj = Cart.objects.get(id = order_id)
    total_cost = (cart_obj.tour.cost)*(cart_obj.head_count)
    context = {
        "cart_obj":cart_obj,
        "total_cost":total_cost 
    }
    return render(request, 'booked_tours_detail.html', context)
    
    
    
    
    
    
    
    
    
    
    
