from django.urls import path
from .views import stripe_success, stripe_cancel, PaymentsListView

urlpatterns = [
    path("success/", stripe_success),
    path("cancel/", stripe_cancel),
    path("payments/", PaymentsListView.as_view(), name="all-payments"),
]

app_name = "payments"
