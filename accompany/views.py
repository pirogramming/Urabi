from django.shortcuts import render
from . import views
from django.views.generic import ListView

# Create your views here.
#class AccompanyListView(ListView):

def accompany_list(request):
    return render(request, 'accompany/accompany_list.html')

def accompany_detail(request):
    return render(request, 'accompany/accompany_detail.html')

def accompany_create(request):
    return render(request, 'accompany/accompany_create.html')