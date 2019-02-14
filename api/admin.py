from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import UserProfile
from api.models import Contact
# Register your models here.
admin.site.register(Contact)
admin.site.register(UserProfile)