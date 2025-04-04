import stripe

from library.models import Borrowing
from library_service import settings
from payment.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = settings.DOMAIN


def create_stripe_session(borrowing: Borrowing):

    total_price = (
        borrowing.expected_return_date - borrowing.borrow_date
    ).days * borrowing.book.daily_free
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(total_price * 100),
                    "product_data": {
                        "name": f"Borrowing Book: {borrowing.book.title}",
                    },
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=YOUR_DOMAIN
        + "/api/library/success/?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=YOUR_DOMAIN + "/api/library/cancel/",
    )

    payment = Payment.objects.create(
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=total_price,
        status=Payment.Status.PENDING,
        type=Payment.Type.PAYMENT,
    )

    return payment
