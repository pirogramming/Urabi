from django.shortcuts import render,redirect,get_object_or_404
from .models import Market,MarketZzim
from .forms import MarketForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .filters import MarketFilter
from users.models import User

def market_list(request):
    queryset = Market.objects.all() 
    filterset = MarketFilter(request.GET, queryset=queryset)  #필터 검색

    filtered_queryset = filterset.qs
    items_per_page = int(request.GET.get('items_per_page', 10)) 

    paginator = Paginator(filtered_queryset, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    selected_status = request.GET.get('status',None)
    selected_category = request.GET.get('category',None)

    return render(request, 'market/market_list.html', 
                    {'markets': page_obj, 'filterset':filterset, 'items_per_page':items_per_page, 'selected_status':selected_status, 'selected_category':selected_category})

    
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

def market_detail(request,item_id):
    market = Market.objects.get(pk=item_id)
    is_zzim = MarketZzim.objects.filter(user=request.user, market=market).exists()
    trust_score = market.user.trust_score
    return render(request, 'market/market_detail.html', {'market':market, 'is_zzim':is_zzim, 'trust_score':trust_score})


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
def market_zzim(request, item_id):

    market = get_object_or_404(Market, pk=item_id)
    zzim, created = MarketZzim.objects.get_or_create(user=request.user, market=market)

    if not created:
        zzim.delete()  # 이미 찜한 경우 삭제
        return JsonResponse({'item_id':market.item_id, "zzim": False})
    
    return JsonResponse({"item_id":market.item_id, "zzim": True})

