from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации и просмотра пользователя"""
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text='Минимум 8 символов'
    )
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone', 'password', 'password_confirm', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def validate_email(self, value):
        """Проверка email на формат"""
        if '@' not in value:
            raise serializers.ValidationError("Email должен содержать символ @")
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Введите корректный email адрес")
        
        return value
    
    def validate_password(self, value):
        """Проверка пароля на сложность"""
        if len(value) < 8:
            raise serializers.ValidationError("Пароль должен содержать минимум 8 символов")
        
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну букву")
        
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну цифру")
        
        return value
    
    def validate(self, data):
        """Проверка совпадения паролей"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                "password_confirm": "Пароли не совпадают"
            })
        return data
    
    def create(self, validated_data):
        """Создание пользователя с хэшированным паролем"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа"""
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})