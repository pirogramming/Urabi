from django.shortcuts import render

def accommodation_filter(request):
    return render(request, 'accommodation/accommodation_filter.html')