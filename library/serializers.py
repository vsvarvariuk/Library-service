from rest_framework import serializers
from library.models import Book, Borrowing
from payment.serializers import PaymentSerializer


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_free")


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="full_name")
    book = serializers.CharField(source="book.title")
    payments = PaymentSerializer()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payments",
        )


class BorrowingReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date", "book", "user")
