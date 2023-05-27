from django.contrib import admin
from .models import UserWithInfo
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(UserWithInfo)