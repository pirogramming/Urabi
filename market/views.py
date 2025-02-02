from django.shortcuts import render,redirect
from .models import Market
from .forms import MarketForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def market_list(request):
    markets = Market.objects.all()  
    return render(request, 'market/market_list.html', {'markets': markets})



# def market_create(request):
#     if request.method == 'GET':
#         form = MarketForm()
#         markets = {'form':form}
#         return render(request, 'market/market_create.html', context = markets)
#     else:
#         form = MarketForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('market:market_list'))
#         else :
#             print(form.errors)
#             print(form.errors.as_json)
#     return render(request, 'market/market_create.html', {'form': form})
@login_required
def market_create(request):
    if request.method == 'POST':
        form = MarketForm(request.POST, request.FILES)
        if form.is_valid():
            market = form.save(commit=False)  # 🚨 데이터 저장 보류
            market.user = request.user  # 🚨 현재 로그인한 사용자 추가
            market.save()  # ✅ user 정보가 포함된 후 저장
            return redirect(reverse('market:market_list'))
        else:
            print(form.errors)
            print(form.errors.as_json())  # 🚨 콘솔에서 오류 메시지 확인

    else:
        form = MarketForm()

    return render(request, 'market/market_create.html', {'form': form})

def market_detail_guest(request):
    return render(request, 'market/market_detail_guest.html')

def market_detail_self(request):
    return render(request, 'market/market_detail_self.html')