import django_filters
from .models import Flash
from django import forms

class FlashFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains", widget=forms.TextInput(attrs={'placeholder':'제목으로 번개 찾기'}))
    tags = django_filters.CharFilter(lookup_expr="icontains",widget=forms.TextInput(attrs={'placeholder':'태그 검색'}))
    date_time = django_filters.DateFilter(lookup_expr='icontains', widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = Flash
        fields = ['title', 'tags', 'date_time']
