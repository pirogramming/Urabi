from django import forms
from .models import Market

class MarketForm(forms.ModelForm):
    class Meta:
        model= Market
        fields = ('__all__')