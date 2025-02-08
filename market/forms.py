from django import forms
from .models import Market
from django.core.exceptions import ValidationError

class MarketForm(forms.ModelForm):
    class Meta:
        model= Market
        exclude = ('created_at', 'updated_at','user')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <=0 :
            raise ValidationError("가격은 0보다 커야 합니다. ")
        return price