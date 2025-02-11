from django import forms
from .models import User, TravelPlan

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'user_gender', 'user_phone', 'profile_image']
        widgets = {
            'user_gender': forms.Select(choices=[('M', 'Male'), ('F', 'Female')]), 
            'profile_image': forms.FileInput(), 
        }

class TravelPlanForm(forms.ModelForm):
    class Meta:
        model = TravelPlan
        fields = ['title', 'city', 'explanation', 'start_date', 'end_date','is_public']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '이름', 'id':'title'}),
            'city': forms.TextInput(attrs={'placeholder': '장소', 'id':'city'}),
            'explanation': forms.Textarea(attrs={'placeholder': '설명을 입력하세요!','id':'explanation'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'id':'start_date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'id':'end_date'}),
        }