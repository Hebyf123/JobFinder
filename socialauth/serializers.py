from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import CustomUser,WORK_TYPES_CHOICES
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        type = serializers.ChoiceField(choices=WORK_TYPES_CHOICES, read_only=True)

        fields = (
            'id', 'email', 'username', 'password', 'role', 'name', 'surname',
            'photo', 'telegram_id', 'company_name', 'type'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'role': {'required': True},
            'company_name': {'required': False},
            'company_address': {'required': False},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', validated_data['email']),
            password=validated_data['password'],
            role=validated_data['role'],
            name=validated_data.get('name', ''),
            surname=validated_data.get('surname', ''),
            photo=validated_data.get('photo', None),
            telegram_id=validated_data.get('telegram_id', None),
            company_name=validated_data.get('company_name', ''),
            type = validated_data.get('type','')
        )
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'role', 'name', 'surname', 'photo', 'telegram_id',
            'company_name', 'type'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.role != 'employer':
            representation.pop('company_name', None)
            representation.pop('company_address', None)
        return representation


class UserRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLES)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise exceptions.AuthenticationFailed('Неверные учетные данные')

            attrs['user'] = user
        else:
            raise exceptions.ValidationError('Email и пароль обязательны для входа')

        return super().validate(attrs)