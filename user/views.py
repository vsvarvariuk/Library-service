from rest_framework import generics
from rest_framework.permissions import AllowAny

from user.serializers import UserSerializer


class UserCreateApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
