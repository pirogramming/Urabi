from django.shortcuts import render, reverse
from . import views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import TravelGroup, TravelParticipants
from .forms import TravelGroupForm

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


class AccompanyCreateView(CreateView):
    model = TravelGroup
    form_class = TravelGroupForm
    template_name = 'accompany/accompany_create.html'
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('accompany:accompany_detail', kwargs={'pk' : self.object.travel_id})
    
class AccompanyDeleteView(DeleteView):
    model = TravelGroup
    template_name = 'accompany/accompany_detail.html'
    success_url = '/accompany/'