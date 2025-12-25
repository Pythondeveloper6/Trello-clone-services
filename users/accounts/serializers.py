from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User, UserProfile


class UserRegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=8, help_text="User password (minimum 8 char)"
    )
    password_confirm = serializers.CharField(
        write_only=True, help_text="User password (minimum 8 char)"
    )

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Password dont match")
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_verified:
                    data["user"] = user
                    return data
                else:
                    raise serializers.ValidationError("User Account is not verified")
            else:
                raise serializers.ValidationError("Authentication faild for this email")
        else:
            raise serializers.ValidationError("Email & password are required")


class UserProfileSerializer(serializers.ModelSerializer):
    # include user information with profile information
    email = serializers.EmailField(source="user.email", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    date_joined = serializers.CharField(source="user.date_joined", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["email", "username", "first_name", "last_name", "date_joined", "bio"]
