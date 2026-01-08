from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile


class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username", "first_name", "last_name"]
    list_filter = ["is_verified", "date_joined"]
    search_fields = ["email", "first_name", "last_name", "username"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["user__email", "user__username", "bio"]


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
