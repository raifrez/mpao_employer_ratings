from django.db import models

# Create your models here.

class PointSystem(models.Model):
    point_type = models.CharField(max_length=6, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])
    value = models.IntegerField()
    threshold_upper = models.IntegerField(default=9999)
    threshold_lower = models.IntegerField()

class StarSystem(models.Model):
    label = models.CharField(max_length=50, null=True)
    value = models.IntegerField()
    threshold_upper = models.IntegerField(default=9999)
    threshold_lower = models.IntegerField()

class EmployerManager(models.Manager):
    def get_queryset(self):
        return super(EmployerManager, self).get_queryset().filter(is_active=True)

class Employer(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = EmployerManager()
    objects_all = models.Manager()

    def __str__(self):
        return f"{self.name}"

class Payment(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    due_date = models.DateField()
    paid_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Rating(models.Model):
    employer = models.OneToOneField(Employer, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    star_rating = models.ForeignKey(StarSystem, on_delete=models.PROTECT, default=0)
    last_paid_date = models.DateField(null=True)
    payment_streak = models.IntegerField(default=0)
    is_suspended = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

class RatingHistory(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='history')
    stars = models.IntegerField()
    streak = models.IntegerField()
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    