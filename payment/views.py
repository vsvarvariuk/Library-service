from rest_framework import generics
from library_service import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment
import stripe


from .serializers import PaymentSerializer, PaymentAdminSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["GET"])
def stripe_success(request):
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    try:
        payment = Payment.objects.get(session_id=session_id)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    if session.payment_status == "paid":
        payment.status = Payment.Status.PAID
        payment.save()

    return Response({"message": "Payment successful!"})


@api_view(["GET"])
def stripe_cancel(request):
    return Response({"message": "Payment was canceled or timed out. Try again later"})


class PaymentsListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Payment.objects.all().select_related("borrowing")
        return Payment.objects.filter(borrowing__user=self.request.user).select_related(
            "borrowing"
        )

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_staff:
            return PaymentAdminSerializer
        return PaymentSerializer
