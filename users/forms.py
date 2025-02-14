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
    """
    TravelPlan에서 딱 'explanation'만 입력받도록 (start_date/end_date는 뷰에서 처리).
    markers/polyline은 자바스크립트로 JSON 입력 후 뷰에서 처리.
    """
    class Meta:
        model = TravelPlan
        fields = ['explanation']  # title/city 없음
        widgets = {
            'explanation': forms.Textarea(attrs={'placeholder':'설명을 입력하세요!'}),
        }
