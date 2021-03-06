from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .forms import UserForm, ProfileForm
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .forms import FindDestinationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


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

