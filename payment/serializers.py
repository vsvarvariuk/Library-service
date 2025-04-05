from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="borrowing.book.title")

    class Meta:
        model = Payment
        fields = (
            "id",
            "book",
            "status",
            "type",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentAdminSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="borrowing.book.title")
    user = serializers.CharField(source="borrowing.full_name")

    class Meta:
        model = Payment
        fields = (
            "id",
            "book",
            "user",
            "status",
            "type",
            "session_url",
            "session_id",
            "money_to_pay",
        )
