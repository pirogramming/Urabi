from django import forms
from .models import User, TravelPlan

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'user_gender', 'user_phone', 'profile_image']
        widgets = {
            'user_gender': forms.Select(choices=[('M','Male'),('F','Female')]),
            'profile_image': forms.FileInput(),
        }

class TravelPlanForm(forms.ModelForm):
    class Meta:
        model = TravelPlan
        fields = ['explanation'] 
        widgets = {
            'explanation': forms.Textarea(attrs={'placeholder':'설명을 입력하세요!'}),
        }
