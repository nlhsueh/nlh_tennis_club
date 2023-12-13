from django.db import models
# User
from django.contrib.auth.models import User
# timezone
from django.utils import timezone

# Create your models here.
class Court(models.Model):  
    COURT_TYPE = [
        ("G", "草地"),
        ("H", "硬地"),
        ("N", "泥地"),
        ("D", "地毯"),
    ]
    courtname = models.CharField(max_length=100)
    courttype = models.CharField(max_length=1, choices=COURT_TYPE)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city} {self.courtname}"  
    
class Booking(models.Model):
    court = models.ForeignKey(Court, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    date = models.DateField(default = timezone.now)

    class Meta:
        unique_together = ('court', 'date')    