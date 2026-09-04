"""
Serializers for authentication and User model management.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for displaying User details."""

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates email format, email uniqueness, password strength,
    and returns user details along with JWT authentication tokens.
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Password must be at least 8 characters long.'
    )

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')

    def validate_password(self, value):
        """Validate password strength using Django's password validators."""
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        validate_password(value)
        return value

    def validate_email(self, value):
        """Ensure email is converted to lowercase and is unique."""
        email = value.lower().strip()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('A user with this email address already exists.')
        return email

    def create(self, validated_data):
        """Create user with hashed password."""
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def to_representation(self, instance):
        """Include JWT access and refresh tokens in the response representation."""
        refresh = RefreshToken.for_user(instance)
        return {
            'user': UserSerializer(instance).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login authentication.
    Validates user credentials and generates JWT access and refresh tokens.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Authenticate user credentials."""
        email = attrs.get('email', '').lower().strip()
        password = attrs.get('password', '')

        if not email or not password:
            raise serializers.ValidationError('Both email and password are required.')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        """Return user data and tokens upon successful login validation."""
        user = self.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
