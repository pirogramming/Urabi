from django.shortcuts import render

# Create your views here.
def market_list(request):
    return render(request, 'market/market_list.html')