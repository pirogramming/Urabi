from django.shortcuts import render
from . import views
from django.views.generic import ListView, DetailView
from .models import TravelGroup, TravelParticipants

# Create your views here.
#class AccompanyListView(ListView):

class AccompanyListView(ListView):
    model = TravelGroup
    template_name = 'accompany/accompany_list.html' 
    ordering = ['-created_at']
    paginate_by = 6

class AccompanyDetailView(DetailView):
    model = TravelGroup
    template_name = 'accompany/accompany_detail.html'

def accompany_create(request):
    return render(request, 'accompany/accompany_create.html')