from datetime import datetime
from main.models import Rating, PointSystem, StarSystem

class Command(BaseCommand):
    help = 'Update employer ratings manually or on a monthly basis'

    def handle(self, *args, **options):
        today = datetime.now().date()

        ratings = Rating.objects.filter(is_suspended=False).all()
        #TODO: Update asychronously in chunks using celery for better performance

        for rating in ratings:
            missed_payments = Payments.objects.filter(
                    employer=rating.employer, 
                    paid_date=None, 
                    due_date__lt=today,
                    created_at__gt=rating.last_paid_date
                )


            due_since_last_pay = missed_payments.order_by('due_date').first()
            if due_since_last_pay:
                overdue = today - due_since_last_pay.due_date
                # Update points
                point_update = PointSystem.objects.filter(
                        point_type='unpaid',
                        threshold_upper__gte=overdue,
                        threshold_lower__lte=overdue
                    ).first()

                rating.points += point_update.value

                max_penalty = PointSystem.objects.order_by('value').first()
                if not max_penalty:
                    self.stderr.write("PointSystem not found. Skipping suspension.")
                elif point_update.value == max_penalty:
                    rating.is_suspended = True

            # Reset stars
            missed_payments_count = missed_payments.count()
            if missed_payments_count > 0:
                rating.payment_streak = 0

                star_update = StarSystem.objects.filter(
                        threshold_upper__gte=rating.payment_streak,
                        threshold_lower__lte=rating.payment_streak  
                    ).first()

                if not star_update:
                    self.stderr.write("Rating for {rating.employer.name} failed. StarSystem not found.")
                    continue

                rating.star_rating = star_update

            updated = rating.save()

            if updated:
                self.stdout.write(self.style.SUCCESS(f'Rating for {rating.employer.name} updated successfully!'))
            else:
                self.stderr.write("Rating for {rating.employer.name} failed.")