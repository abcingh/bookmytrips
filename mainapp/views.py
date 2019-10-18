from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .forms import UserForm, ProfileForm
from django.conf import settings



User = settings.AUTH_USER_MODEL



# Create your views here.
def index(request):
    return render(request, 'index.html')

# Create your views here.
def profile(request):
    username = request.user.username
    user_obj = User.objects.get(username = username)
    context = {
        "user_obj": user_obj,
    }
    return render(request, 'profile.html', context)


def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/profile/')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
