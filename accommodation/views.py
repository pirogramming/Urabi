from django.shortcuts import render

def accommodation_filter(request):
    return render(request, 'accommodation/accommodation_filter.html')

def location_view(request):
    return render(request, 'accommodation/accommodation_location.html')
