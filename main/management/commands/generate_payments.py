from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from main.models import Employer, Payment
from main.serializers import PaymentSerializer
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    #TODO: add cron job
    help = 'Generate payment invoices on a monthly basis'

    def handle(self, *args, **options):
        today = datetime.now().date()
        day = 15
        month = today.month
        year = today.year

        due_date = date(year, month, day)

        employers = Employer.objects.all()

        data = []

        for employer in employers:
            if not Payment.objects.filter(due_date__month=month, employer=employer).exists():
                data.append({
                    "employer": employer.id,
                    "amount": None,
                    "due_date": due_date,
                    "paid_date": None
                })
        payment_serializer = PaymentSerializer(data=data, many=True)
        payment_serializer.is_valid(raise_exception=True)
        result = payment_serializer.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {len(result)} payments!'))
        
