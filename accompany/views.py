from django.shortcuts import render, reverse, redirect
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
        travel_groups = context['object_list']
        for travel in travel_groups:
            travel.tags = travel.tags.split(',') if travel.tags else []
            travel.current_participants = travel.participants.count() 
        context['tags'] = travel_groups
        return context

class AccompanyDetailView(DetailView):
    model = TravelGroup
    template_name = 'accompany/accompany_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_zzims = Accompany_Zzim.objects.filter(user=self.request.user)
            zzim_items = [zzim.item for zzim in user_zzims]
            context['zzim_items'] = zzim_items
        else:
            context['zzim_items'] = []
        group = context['object']
        users = User.objects.all().exclude(pk=group.created_by.pk)
        participants = TravelParticipants.objects.filter(travel=group)
        users = users.exclude(pk__in=[participant.user.pk for participant in TravelParticipants.objects.filter(travel=group)])
        context['users'] = users
        context['participants'] = participants
        if group.tags:
            group_tags = group.tags.split(',')
            context['tags'] = group_tags 

        return context

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

@login_required
@csrf_exempt
def add_participant(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            travel_id = data.get("travel_id")
            user_id = data.get("user_id")

            travel = get_object_or_404(TravelGroup, travel_id=travel_id)
            user = get_object_or_404(User, id=user_id)

            # 중복 참가 방지
            if TravelParticipants.objects.filter(travel=travel, user=user).exists():
                return JsonResponse({"message": "이미 참가 중입니다."}, status=400)

            # 최대 인원 초과 방지
            if travel.participants.count() >= travel.max_member:
                return JsonResponse({"message": "최대 인원을 초과했습니다."}, status=400)

            # 참가자 추가
            TravelParticipants.objects.create(travel=travel, user=user)
            travel.now_member += 1
            travel.save()
            return JsonResponse({"message": "참가 완료!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

@login_required
@csrf_exempt
def remove_participant(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            travel_id = data.get("travel_id")
            user_id = data.get("user_id")

            travel = get_object_or_404(TravelGroup, travel_id=travel_id)
            user = get_object_or_404(User, id=user_id)

            # 참가자 삭제
            TravelParticipants.objects.filter(travel=travel, user=user).delete()
            travel.now_member -= 1
            travel.save()
            return JsonResponse({"message": "참가 취소!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "잘못된 요청입니다."}, status=400)