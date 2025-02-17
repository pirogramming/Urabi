from django.shortcuts import render, reverse, redirect
from . import views
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import TravelGroup, TravelParticipants, Accompany_Zzim, AccompanyRequest
from .forms import TravelGroupForm
from users.models import User, TravelPlan, TravelSchedule
from .filters import AccompanyFilter

# Create your views here.
#class AccompanyListView(ListView):

class AccompanyListView(ListView):
    model = TravelGroup
    template_name = 'accompany/accompany_list.html' 
    ordering = ['-created_at']
    paginate_by = 6
    zzim_list = Accompany_Zzim.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        
        self.filterset = AccompanyFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        if self.request.user.is_authenticated:
            user_zzims = Accompany_Zzim.objects.filter(user=self.request.user)
            zzim_items = [zzim.item for zzim in user_zzims]
            context['zzim_items'] = zzim_items
        else:
            context['zzim_items'] = []
            
        travel_groups = context['object_list']
        for travel in travel_groups:
            travel.tags = travel.tags.split(',') if travel.tags else []
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
        participants = TravelParticipants.objects.filter(travel=group)
        participant_users = [participant.user for participant in participants]  # User 객체 리스트로 변환
        requested_users = User.objects.filter(user_requests__travel=group)
        if group.this_plan_id:
            this_plan = get_object_or_404(TravelPlan, pk=group.this_plan_id)
            context['this_plan'] = this_plan
            this_schedule = this_plan.schedule
            context['travel_plans'] = TravelPlan.objects.filter(schedule=this_schedule)

        context['users'] = requested_users
        context['participants'] = participant_users
        if group.tags:
            group_tags = group.tags.split(',')
            context['tags'] = group_tags
        
        # 마커와 폴리라인 데이터를 JSON 형식으로 전달
        context['markers'] = group.markers
        context['polyline'] = group.polyline

        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY

        return context
    
def load_plan_data(request):
    plan_id = request.GET.get('plan_id')
    if plan_id:
        travel_plan = get_object_or_404(TravelPlan, pk=plan_id)
        data = {
            'markers': travel_plan.markers,
            'polyline': travel_plan.polyline,
            'title': travel_plan.title,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid plan_id'}, status=400)

class AccompanyCreateView(CreateView):
    model = TravelGroup
    form_class = TravelGroupForm
    template_name = 'accompany/accompany_form.html'

    def get_initial(self):
        initial = super().get_initial()
        plan_id = self.request.GET.get('plan_id')
        if plan_id:
            travel_plan = get_object_or_404(TravelPlan, pk=plan_id)
            initial.update({
                'explanation': travel_plan.explanation,
                'start_date': travel_plan.start_date,
                'end_date': travel_plan.end_date,
                'this_plan_id': travel_plan.plan_id,
            })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_id = self.request.GET.get('plan_id')
        if plan_id:
            travel_plan = get_object_or_404(TravelPlan, pk=plan_id)
            context['this_plan'] = travel_plan
        context['travel_schedules'] = TravelSchedule.objects.filter(user=self.request.user)
        context['travel_plans'] = TravelPlan.objects.filter(created_by=self.request.user)

        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        # 마커와 폴리라인 데이터를 처리
        markers_data = self.request.POST.get('markers')
        polyline_data = self.request.POST.get('polyline')
        plan_id = self.request.GET.get('plan_id')
        if plan_id:
            form.instance.this_plan_id = plan_id

        form.instance.markers = markers_data
        form.instance.polyline = polyline_data
        

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accompany:accompany_detail', kwargs={'pk': self.object.travel_id})

class AccompanyUpdateView(UpdateView):
    model = TravelGroup
    form_class = TravelGroupForm
    template_name = 'accompany/accompany_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self._original_this_plan_id = obj.this_plan_id
        self._original_call_schedule = obj.call_schedule
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_id = self.request.GET.get('plan_id')
        if plan_id:
            travel_plan = get_object_or_404(TravelPlan, pk=plan_id)
            context['this_plan'] = travel_plan
        context['travel_schedules'] = TravelSchedule.objects.filter(user=self.request.user)
        context['travel_plans'] = TravelPlan.objects.filter(created_by=self.request.user)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        markers_data = self.request.POST.get('markers')
        polyline_data = self.request.POST.get('polyline')

        form.instance.this_plan_id = self._original_this_plan_id
        form.instance.call_schedule = self._original_call_schedule

        form.instance.markers = markers_data
        form.instance.polyline = polyline_data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accompany:accompany_detail', kwargs={'pk': self.object.travel_id})

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

            del_data = AccompanyRequest.objects.filter(travel=travel, user=user)
            del_data.delete()

            # 중복 참가 방지
            if TravelParticipants.objects.filter(travel=travel, user=user).exists():
                return JsonResponse({"message": "이미 참가 중입니다."}, status=400)

            # 최대 인원 초과 방지
            if travel.travel_participants.count() >= travel.max_member:
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

            AccompanyRequest.objects.filter(travel=travel, user=user).delete()
            return JsonResponse({"message": "참가 취소!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

@csrf_exempt
@login_required
def apply_participant(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            travel_id = data.get("travel_id")
            accompany = TravelGroup.objects.get(travel_id=travel_id)
            # 중복 참가 방지
            if TravelParticipants.objects.filter(travel=accompany, user=request.user).exists():
                return JsonResponse({"success": False, "message": "이미 참가 신청을 했습니다."}, status=400)
            
            # 참가자 추가
            AccompanyRequest.objects.create(travel=accompany, user=request.user)
            
            return JsonResponse({"success": True, "message": "참가 신청이 완료되었습니다!"})
        except TravelGroup.DoesNotExist:
            return JsonResponse({"success": False, "message": "해당 여행을 찾을 수 없습니다."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "잘못된 요청입니다."}, status=400)

@csrf_exempt
@login_required
def cancel_participant(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            travel_id = data.get("travel_id")
            accompany = TravelGroup.objects.get(travel_id=travel_id)
            
            # 참가 신청 취소
            AccompanyRequest.objects.filter(travel=accompany, user=request.user).delete()
            
            return JsonResponse({"success": True, "message": "참가 신청이 취소되었습니다."})
        except TravelGroup.DoesNotExist:
            return JsonResponse({"success": False, "message": "해당 여행을 찾을 수 없습니다."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "잘못된 요청입니다."}, status=400)