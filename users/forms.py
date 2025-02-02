from django import forms
from .models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'nickname', 'user_gender', 'user_phone', 'profile_image']
        widgets = {
            'user_gender': forms.Select(choices=[('M', 'Male'), ('F', 'Female')]), 
            'profile_image': forms.FileInput(), 
        }
