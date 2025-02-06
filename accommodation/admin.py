from django.contrib import admin
from .models import AccommodationReview, ReviewComment

@admin.register(AccommodationReview)
class AccommodationReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'accommodation_name', 'city', 'category', 'rating', 'user', 'created_at')
    list_filter = ('city', 'category', 'rating')
    search_fields = ('accommodation_name', 'city', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'review', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'review__accommodation_name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
