from django.shortcuts import render, reverse
from . import views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import TravelGroup, TravelParticipants, Accompany_Zzim
from .forms import TravelGroupForm
from users.models import User

# Create your views here.
#class AccompanyListView(ListView):

class AccompanyListView(ListView):
    model = TravelGroup
    template_name = 'accompany/accompany_list.html' 
    ordering = ['-created_at']
    paginate_by = 6
    zzim_list = Accompany_Zzim.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_zzims = Accompany_Zzim.objects.filter(user=self.request.user)
            zzim_items = [zzim.item for zzim in user_zzims]
            context['zzim_items'] = zzim_items
        else:
            context['zzim_items'] = []
        
        return context

class AccompanyDetailView(DetailView):
    model = TravelGroup
    template_name = 'accompany/accompany_detail.html'


class AccompanyCreateView(CreateView):
    model = TravelGroup
    form_class = TravelGroupForm
    template_name = 'accompany/accompany_form.html'
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('accompany:accompany_detail', kwargs={'pk' : self.object.travel_id})

class AccompanyUpdateView(UpdateView):
    model = TravelGroup
    form_class = TravelGroupForm
    template_name = 'accompany/accompany_form.html'
    def get_success_url(self):
        return reverse('accompany:accompany_detail', kwargs={'pk' : self.object.travel_id})

class AccompanyDeleteView(DeleteView):
    model = TravelGroup
    template_name = 'accompany/accompany_detail.html'
    success_url = '/accompany/'

@login_required
@csrf_exempt
def toggle_zzim(request, travel_id):
    travel = get_object_or_404(TravelGroup, pk=travel_id)
    zzim, created = Accompany_Zzim.objects.get_or_create(user=request.user, item=travel)

    if not created:
        # 이미 찜한 경우 삭제
        zzim.delete()
        return JsonResponse({'travel_id':travel.travel_id, 'zzim': False})  # False면 찜이 해제된 상태

    return JsonResponse({'zzim': True})  # True면 찜한 상태