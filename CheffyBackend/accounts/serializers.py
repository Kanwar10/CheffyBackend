# users/serializers.py
from rest_framework import serializers
from .models import *
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserLoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number", None)
        password = data.get("password", None)
        user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this phone number and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given phone number and password does not exists'
            )
        return {
            'phone_number': user.phone_number,
            'token': jwt_token
        }


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number',  'password','user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = CustomUser
        fields = ('id', 'phone_number', 'email', 'password', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}


class CustomerProfileSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = CustomerProfile
        fields = ('id', 'user', 'email', 'fullname', 'gender',
                  'address', 'flat_no', 'landmark')


class PartnerProfileSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = PartnerProfile
        fields = ('id','user', 'email', 'fullname','gender','qualification','place_of_work',
        'yex')

