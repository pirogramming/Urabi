import django_filters
import django_filters.widgets
from .models import TravelGroup
from django import forms

class AccompanyFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='icontains', label="searching_city", widget=forms.TextInput(attrs={'placeholder' : '장소 검색으로 동행 찾기 (ex. 프랑스 파리)'}))
    start_date = django_filters.DateFilter(lookup_expr='exact', label="searching_startDate",widget=forms.DateInput(attrs={'type':'date'}) )
    end_date = django_filters.DateFilter(lookup_expr='exact', label="searching_endDate", widget=forms.DateInput(attrs={'type':'date'}))
    gender = django_filters.ChoiceFilter(choices=TravelGroup.GENDER_CHOICES, label="searching_gender")
    age = django_filters.NumberFilter(method = "filtered_age", widget=forms.NumberInput(attrs={'type':'number', 'placeholder':'나이'}))


    class Meta:
        model = TravelGroup
        fields = ['city', 'start_date', 'end_date', 'gender', 'age']


    def filtered_age(self, queryset, name, value):
        return queryset.filter(min_age__lte=value, max_age__gte=value)