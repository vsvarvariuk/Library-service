from datetime import date

from django_q.models import Schedule
from django_q.tasks import schedule, async_task
from library.models import Borrowing
from telegram.helper import send_telegram_message


def check_overdue_borrowings():
    today = date.today()
    overdue = Borrowing.objects.filter(
        expected_return_date__lt=today, actual_return_date__isnull=True
    )

    if not overdue.exists():
        send_telegram_message("No borrowings overdue today!")
        return

    for b in overdue:
        msg = (
            f"*Overdue Borrowing!*\n\n"
            f"User: {b.user.email}\n"
            f"Book: {b.book.title}\n"
            f"Should return: {b.expected_return_date}"
        )
        send_telegram_message(msg)


def send_borrowing_created_notification(borrowing):
    message = (
        f"*New Borrowing Created!*\n\n"
        f"User: {borrowing.full_name}\n"
        f"Book: {borrowing.book.title}\n"
        f"From: {borrowing.borrow_date}\n"
        f"To: {borrowing.expected_return_date}"
    )
    send_telegram_message(message)
