from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from .forms import UserForm, ProfileForm
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .forms import FindDestinationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Tour, Cart
from django.contrib import messages



User = get_user_model()


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = FindDestinationForm(request.POST)
        if form.is_valid():
            place = form.cleaned_data['place']
            print(place)
        # return HttpResponse('Form Called')
    form = FindDestinationForm()
    return render(request, 'index.html', {'form': form})

@login_required
def profile(request):
    username = request.user.username
    user_obj = User.objects.get(username = username)
    context = {
        "user_obj": user_obj,
    }
    return render(request, 'profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
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
    if request.method =="POST":
        head_count = request.POST.get("head_count")
        tour_date = request.POST.get("tour_date")
        tour = get_object_or_404(Tour, id=tour_id)
        user = request.user
        cart = Cart.objects.create(head_count = head_count, tour_date = tour_date, user=request.user)
        cart.save()
        # =========>do some thing to get all cart value object
        
        cart_id ="quesyset[::-1]"
        messages.success(request,'Items added to cart')
        return redirect("/checkout/"+str())
    return render(request, 'profile.html')
    # return redirect(reverse('checkout'))


def checkout(request, cart_id):
    if request.method =="POST":
        
        # cart = Cart.objects.all()[::-1]
        context = {
            "cart":cart
        }
        return render(request, 'checkout.html', context)

def checkout_complete(request):
    #some process for checking out
    return 





    # if request.method =="POST":
    #     content_title = request.POST.get("content_title")
    #     cotegory = request.POST.get("content_category")
    #     content_body = request.POST.get("content_body")

    #     data = Data()
    #     data.user = request.user
    #     data.content_title = content_title
    #     data.cotegory = cotegory
    #     data.content_body = content_body
    #     data.save()
    #     messages.success(request,'Thank you for submitting your creation  -Team VISMRITA')
    #     return redirect("/submit_creation/")
    # return render(request,"profiles/submit_creation.html",{})


    # head_count = models.IntegerField(default = 0)
    # tour_date = models.DateField()
    # user = models.ForeignKey(User, on_delete= models.CASCADE)
    # tour = models.ForeignKey(Tour, on_delete = models.CASCADE)



