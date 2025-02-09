from django import forms
from .models import Market
from django.core.exceptions import ValidationError

class MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        exclude = ('created_at', 'updated_at', 'user')
        widgets = {
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '도시명을 입력하세요'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목'
            }),
            'explanation': forms.Textarea(attrs={
                'id': 'mkt_explanation',
                'placeholder': '상품 설명을 입력하세요',
                'rows': 5
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '가격을 입력하세요'
            }),
            'photo': forms.ClearableFileInput(attrs={'class': 'file-upload-input', 'id':'image-upload'}),

            
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <=0 :
            raise ValidationError("가격은 0보다 커야 합니다. ")
        return price