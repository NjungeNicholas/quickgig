from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import BaseUser, TaskerProfile
from services.models import Service


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = BaseUser
        fields = ('email', 'username', 'location', 'phone_number', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = BaseUser.objects.create_user(**validated_data)
        user.is_active = True  # Activate user immediately or set to False for email verification
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                              username=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            attrs['user'] = user
            validated_data = super().validate(attrs)
            validated_data['user'] = user
            return validated_data
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_tasker'] = user.is_tasker
        token['is_client'] = user.is_client
        return token


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing user profile"""
    class Meta:
        model = BaseUser
        fields = ('id', 'email', 'username', 'location', 'phone_number', 
                 'profile_picture', 'is_client', 'is_tasker')
        read_only_fields = ('id', 'email', 'is_client', 'is_tasker')


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    class Meta:
        model = BaseUser
        fields = ('username', 'location', 'phone_number', 'profile_picture')

    def validate_username(self, value):
        user = self.context['request'].user
        if BaseUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.location = validated_data.get('location', instance.location)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance


class BecomeTaskerSerializer(serializers.Serializer):
    """Serializer for converting a user to a tasker"""
    bio = serializers.CharField(max_length=1000, required=True)
    skills = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Service.objects.all()),
        required=True,
    )

    def update(self, instance, validated_data):
        # Update user to be a tasker
        instance.is_tasker = True
        instance.save()

        # The signal will automatically create the TaskerProfile
        # Now get the profile and update it
        tasker_profile = instance.taskerprofile
        
        # Update profile with provided data
        if 'bio' in validated_data:
            tasker_profile.bio = validated_data['bio']
        
        if 'skills' in validated_data:
            tasker_profile.skills.set(validated_data['skills'])
        
        tasker_profile.save()
        return instance


class TaskerProfileSerializer(serializers.ModelSerializer):
    """Serializer for tasker profile"""
    skills = serializers.StringRelatedField(many=True, read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = TaskerProfile
        fields = ('id', 'user', 'bio', 'skills')


class TaskerProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating tasker profile"""
    skills = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Service.objects.all()),
        required=True,
    )

    class Meta:
        model = TaskerProfile
        fields = ('bio', 'skills')


    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        
        if 'skills' in validated_data:
            instance.skills.set(validated_data['skills'])
        
        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for changing user password"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New password fields didn't match.")
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user