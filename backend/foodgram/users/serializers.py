from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for creation, subscription of users."""

    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=50, required=True)
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    is_subscribed = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_is_subscribed(self, obj):
        """Return subscription status."""
        user = self.context['request'].user
        if user.is_authenticated:
            user = self.context['request'].user
            author = obj
            return Subscription.objects.filter(
                user=user, author=author).exists()
        return None

    def create(self, validated_data):
        """Create new Users."""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'password', 'is_subscribed']
        read_only_fields = ['id']


class CurrentUserSerializer(serializers.Serializer):
    """Serialize 'me' requests."""

    email = serializers.EmailField()
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    is_subscribed = serializers.CharField(default=False)


class ChangePasswordSerializer(serializers.Serializer):
    """Serialize password change requests."""

    model = User

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
