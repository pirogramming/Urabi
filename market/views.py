from django.shortcuts import render,redirect
from .models import Market
from .forms import MarketForm
from django.urls import reverse

# Create your views here.
def market_list(request):
    return render(request, 'market/market_list.html')


def market_create(request):
    if request.method == 'GET':
        form = MarketForm()
        markets = {'form':form}
        return render(request, 'market/market_create.html', context = markets)
    else:
        form = MarketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect(reverse('market:market_list'))
    

def market_detail_guest(request):
    return render(request, 'market/market_detail_guest.html')

def market_detail_self(request):
    return render(request, 'market/market_detail_self.html')