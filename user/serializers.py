from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from restaurant.models import Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', )
        read_only_fields = ('id', 'created_time', 'updated_time')


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['user_id', 'created_time', 'updated_time'] 


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
        )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if len(attrs['password']) > 16 or len(attrs['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be a string between 8 and 16 letters."})
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", attrs['password']):
            raise serializers.ValidationError({"password": "Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user