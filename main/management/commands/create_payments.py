from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from main.models import Employer, Payment
from main.serializers import PaymentSerializer

class Command(BaseCommand):
    #TODO: add cron job
    help = 'Generate payment invoices on a monthly basis'

    def handle(self, *args, **options):
        today = datetime.now().date()
        day = 15
        month = today.month
        year = today.year

        due_date = date(year, month, day)
        if today.day > 15:
            due_date = due_date + relativedelta(months=1)

        employers = Employer.objects.all()

        data = []

        for employer in  employers:
            data.append({
                "employer": employer,
                "amount": None,
                "due_date": due_date,
                "paid_date": None
            })
        payment_serializer = PaymentSerializer(data=data, many=True)
        try:
            payment_serializer.is_valid()
        except Exception as e:
            self.stderr.write(f"Payment generation failed. {e}")
            return

        payment_serializer.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {len(data)} updated successfully!'))
        
