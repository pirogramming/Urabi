from django import forms
from .models import TravelGroup

class TravelGroupForm(forms.ModelForm):
    class Meta:
        model = TravelGroup
        fields = ['title', 'city', 'explanation', 'start_date', 'end_date', 'max_member', 'tags', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목', 'id':'title'}),
            'city': forms.TextInput(attrs={'placeholder': '도시', 'id':'city'}),
            'explanation': forms.Textarea(attrs={'placeholder': '설명을 입력하세요!','id':'description'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'max_member': forms.NumberInput(attrs={'placeholder': '최대 인원', 'id':'max_member'}),
            'tags': forms.Textarea(attrs={'placeholder': '장소 태그', 'id':'tags'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'file-upload-input', 'id':'image-upload'}),
        }
