from django.db import models
from users.models import User

# Create your models here.
class TravelGroup(models.Model):
    travel_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    explanation = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_travels')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    max_member = models.IntegerField()
    tags = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='static/travel_photos/', null=True, blank=True)
    def __str__(self):
        return self.title

class TravelParticipants(models.Model):
    id = models.BigAutoField(primary_key=True)
    travel = models.ForeignKey(TravelGroup, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')

    def __str__(self):
        return f"Participant {self.user.email} in {self.travel.title}"