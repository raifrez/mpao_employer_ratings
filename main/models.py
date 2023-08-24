from django.db import models

# Create your models here.
class Employer(models.Model):
    name = models.CharField(max_length=3)
    joined_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


