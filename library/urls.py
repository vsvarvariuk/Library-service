from django.urls import path, include
from rest_framework import routers
from library.views import BookViewSet, BorrowingViewSet, BorrowingReturnView
router = routers.DefaultRouter()
router.register("books", BookViewSet)

router.register("borrowings", BorrowingViewSet,)
urlpatterns = [
    path("", include(router.urls)),
    path("borrowings/<int:pk>/return/", BorrowingReturnView.as_view(), name="borrowing-return"),
]
app_name = "library"
