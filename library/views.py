from datetime import datetime
from django.db.models import Q
from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from library.models import Book, Borrowing
from library.serializers import (
    BookSerializer,
    BorrowingSerializer,
    BorrowingListDetailSerializer,
    BorrowingReturnSerializer,
)
from payment.stripe import create_stripe_session


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        if self.request.user.is_staff:
            full_name = self.request.query_params.get("user")
            is_active = self.request.query_params.get("is_active")
            if full_name:
                queryset = queryset.filter(
                    Q(user__first_name__icontains=full_name)
                    | Q(user__last_name__icontains=full_name)
                )
            if is_active and is_active == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            if is_active and is_active == "false":
                queryset = (
                    queryset.filter(actual_return_date__isnull=False)
                    .select_related("book", "user")
                    .prefetch_related("payments")
                )
        else:
            queryset = (
                queryset.filter(user=self.request.user)
                .select_related("book", "user")
                .prefetch_related("payments")
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingSerializer
        return BorrowingListDetailSerializer

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        book = serializer.validated_data["book"]
        if book.inventory <= 0:
            raise ValidationError("This book is no longer available for rental.")

        book.inventory -= 1
        book.save()

        payment = create_stripe_session(borrowing)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this item.")
        return super().destroy(request, *args, **kwargs)


class BorrowingReturnView(generics.UpdateAPIView):
    serializer_class = BorrowingReturnSerializer
    permission_classes = (IsAdminUser,)
    queryset = Borrowing.objects.all()

    def perform_update(self, serializer):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            raise ValidationError("This book has already been returned.")

        borrowing.book.inventory += 1
        datetime_value = datetime.now()
        date_value = datetime_value.date()
        borrowing.actual_return_date = date_value
        borrowing.book.save()

        serializer.save(actual_return_date=borrowing.actual_return_date)
