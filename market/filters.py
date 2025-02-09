import django_filters
from .models import Market
from django import forms

class MarketFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr = 'icontains', label="searching_title" ,widget=forms.TextInput(attrs={'class':'market_filterInput','placeholder' : '제목으로 검색하기'}))
    city =django_filters.CharFilter(lookup_expr='icontains', label="searching_city" ,widget=forms.TextInput(attrs={'class':'market_filterInput','placeholder' : '장소로 검색하기 ( ex. 프랑스 파리 )'}))
    status = django_filters.ChoiceFilter(choices=Market.TRADE_STATUS_CHOICES, label="searching_status" ,widget=forms.Select(attrs={'class': 'market_filterInput'}))
    category = django_filters.ChoiceFilter(choices=Market.CATEGORY_CHOICES, label ="searching_category" ,widget=forms.Select(attrs={'class': 'market_filterInput'}))
    trade_type = django_filters.ChoiceFilter(choices = Market.TRADE_TYPE_CHOICES, label="searching_tradeType", widget=forms.Select(attrs={'class': 'market_filterInput'}))

    class Meta:
        model = Market
        fields = ['title','city','status','category']