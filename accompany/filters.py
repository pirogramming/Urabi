import django_filters
from .models import TravelGroup
from django import forms

class AccompanyFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='icontains', label="searching_city", widget=forms.TextInput(attrs={'placeholder' : '국가, 도시'}))
    start_date = django_filters.DateFilter(lookup_expr='exact', label="searching_startDate",widget=forms.DateInput(attrs={'type':'date'}) )
    end_date = django_filters.DateFilter(lookup_expr='exact', label="searching_endDate", widget=forms.DateInput(attrs={'type':'date'}))
    gender = django_filters.ChoiceFilter(choices=TravelGroup.GENDER_CHOICES, label="searching_gender")
    #나이 추가하기

    class Meta:
        model = TravelGroup
        fields = ['city', 'start_date', 'end_date', 'gender']