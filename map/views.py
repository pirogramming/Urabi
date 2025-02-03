from django.shortcuts import render
from django.http import JsonResponse
from .models import Map

def get_locations(request):
    print("✅ `get_locations` 함수 실행됨") 
    locations = Map.objects.all().values("name", "latitude", "longitude")

    print("get_location 응답: ",locations)
    return JsonResponse(list(locations), safe=False)
