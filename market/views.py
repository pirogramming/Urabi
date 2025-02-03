from django.shortcuts import render,redirect,get_object_or_404
from .models import Market
from .forms import MarketForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import MarketZzim
from django.http import JsonResponse


def market_list(request):
    queryset = Market.objects.all()  

    items_per_page = int(request.GET.get('items_per_page', 10)) 

    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'market/market_list.html', {'markets': page_obj, 'items_per_page':items_per_page})


@login_required
def market_create(request):
    if request.method == 'POST':
        form = MarketForm(request.POST, request.FILES)
        if form.is_valid():
            market = form.save(commit=False)  
            market.user = request.user 
            market.save()  
            return redirect(reverse('market:market_list'))
    else:
        form = MarketForm()

    return render(request, 'market/market_create.html', {'form': form})

def market_detail(request,pk):
    market = Market.objects.get(item_id=pk)
    trust_score = market.user.trust_score
    return render(request, 'market/market_detail.html', {'market':market, 'trust_score':trust_score})


def market_update(request,pk):
    market = Market.objects.get(item_id=pk)
    if request.method == 'GET':
        form = MarketForm(instance=market)    
        return render(request, 'market/market_update.html', {'form':form, 'market':market})
    else:
        form = MarketForm(request.POST, request.FILES, instance=market)
        if form.is_valid():      
            form.save()
            return redirect(reverse('market:market_detail', kwargs={'pk': market.item_id}))
    return render(request, 'market/market_update.html', {'form':form, 'market':market})


def market_delete(request, pk):
    market = Market.objects.get(item_id = pk)
    market.delete()
    return redirect(reverse('market:market_list'))


@login_required
def market_zzim(request, pk):

    market = get_object_or_404(Market, pk=pk)
    user = request.user

    zzim, created = MarketZzim.objects.get_or_create(user=user, market=market)

    if not created:
        zzim.delete()  # 이미 찜한 경우 삭제
        return JsonResponse({"zzimmed": False})
    
    return JsonResponse({"zzimmed": True})
