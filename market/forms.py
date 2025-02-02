from django import forms
from .models import Market

class MarketForm(forms.ModelForm):
    class Meta:
        model= Market
        exclude = ('created_at', 'updated_at','user')