from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse, HttpResponse
from .forms import FindDestinationForm


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
