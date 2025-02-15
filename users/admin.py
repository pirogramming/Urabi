from django.contrib import admin
from .models import User, TravelPlan, TravelSchedule

admin.site.register(TravelPlan)
admin.site.register(TravelSchedule)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nickname', 'user_age', 'user_gender', 'created_at')
    search_fields = ('email', 'nickname')  # 검색 기능 추가
    list_filter = ('user_gender', 'created_at')  # 필터 기능 추가
    readonly_fields = ('created_at',)  # 생성일자는 수정 불가능하게 설정 