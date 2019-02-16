from rest_framework import serializers
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission, IsAuthenticated

# Create your models here. 
class Contact(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=95)
    phone = models.CharField(max_length = 20)
    info = models.CharField(max_length = 500)
    category = models.CharField(max_length = 20)
    icon = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lng = models.DecimalField(max_digits=10, decimal_places=7)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ()
        
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    saved_locations = models.ManyToManyField(Contact)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('saved_locations',)
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        new_profile = UserProfile.objects.create(user=user)
        location = profile_data["saved_locations"]
        for x in location:
            new_profile.saved_locations.add(x)
        new_profile.save()
        
        return user
        
    def update(self, instance, validated_data):
        
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        
        profile.saved_locations.set(profile_data.get('saved_locations', profile.saved_locations))
        profile.save()
        
        return instance