from django.shortcuts import render

# Create your views here.
def market_list(request):
    return render(request, 'market/market_list.html')


def market_create(request):
    return render(request, 'market/market_create.html')

def market_detail_guest(request):
    return render(request, 'market/market_detail_guest.html')

def market_detail_self(request):
    return render(request, 'market/market_detail_self.html')