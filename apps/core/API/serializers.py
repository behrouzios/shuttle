from apps.core.models import CustomUser, UploadedFile, EmailTemplate
from rest_framework import serializers
from django.contrib.auth import authenticate
import re


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'confirm_password', 'national_id']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})
        return data

    def validate_national_id(self, value):
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("National ID must be exactly 10 digits.")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            national_id=validated_data.get('national_id')
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        data['user'] = user
        return data


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file', 'uploaded_at']
        read_only_fields = ['uploaded_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data['user'] = request.user
        return super().create(validated_data)


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'name', 'subject', 'body', 'created_at', 'updated_at']
