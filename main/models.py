from django.db import models

# Create your models here.

class PointSystem(models.Model):
    value = models.IntegerField()
    threshold_upper = models.IntegerField(null=True)
    threshold_lower = models.IntegerField()

class StarSystem(models.Model):
    label = models.CharField(max_length=15, null=True)
    value = models.IntegerField()
    threshold_upper = models.IntegerField(null=True)
    threshold_lower = models.IntegerField()



class Employer(models.Model):
    name = models.CharField(max_length=150)
    joined_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

class Payment(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    due_date = models.DateField()
    paid_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Rating(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    star_rating = models.ForeignKey(StarSystem, on_delete=models.PROTECT)
    last_paid_date = models.DateField(null=True)
    payment_streak = models.IntegerField(default=0)
    is_suspended = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

class RatingHistory(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    stars_change = models.IntegerField()
    streak_change = models.IntegerField()
    point_change = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    