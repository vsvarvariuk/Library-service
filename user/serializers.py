from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "password", "is_staff", )
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password_data = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password_data:
            user.set_password(password_data)
        user.save()
        return user