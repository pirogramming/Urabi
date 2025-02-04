import django_filters
from .models import Market

class MarketFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr = 'icontains', label="searching_title")
    city =django_filters.CharFilter(lookup_expr='icontains', label="searching_city")
    status = django_filters.ChoiceFilter(choices=Market.TRADE_STATUS_CHOICES, label="searching_status")
    category = django_filters.ChoiceFilter(choices=Market.CATEGORY_CHOICES, label ="searching_category")

    class Meta:
        model = Market
        fields = ['title','city','status','category']