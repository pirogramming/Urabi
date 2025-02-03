from django.shortcuts import render
from django.http import JsonResponse
from .models import Map

def get_locations(request):
    locations = Map.objects.all().values("name", "latitude", "longitude")
    return JsonResponse(list(locations), safe=False)
