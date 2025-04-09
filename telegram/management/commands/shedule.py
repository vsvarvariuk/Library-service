from django.core.management.base import BaseCommand
from django_q.models import Schedule

class Command(BaseCommand):
    help = "Create schedule for checking overdue borrowings"

    def handle(self, *args, **kwargs):
        schedule, created = Schedule.objects.get_or_create(
            func="telegram.views.check_overdue_borrowings",
            schedule_type=Schedule.MINUTES,
            minutes=1,
            name="Check Overdue Borrowings Every Minute"
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✅ Schedule created successfully!"))
        else:
            self.stdout.write("ℹ️ Schedule already exists.")