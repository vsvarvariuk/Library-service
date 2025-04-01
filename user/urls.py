from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import UserCreateApiView, ManageUserApiView

urlpatterns = [
    path("users/", UserCreateApiView.as_view(), name="create-user"),
    path("me/", ManageUserApiView.as_view(), name="me"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
app_name = "user"
