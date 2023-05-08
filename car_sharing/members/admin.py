from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'creation_at', 'updated_at']

admin.site.register(CustomUser, CustomUserAdmin)