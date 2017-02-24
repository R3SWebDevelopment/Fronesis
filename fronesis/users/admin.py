from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import register, TabularInline
from django.contrib.auth.models import User
from fronesis.admin import admin_site
from .models import UserProfile


class UserProfileInline(TabularInline):
    model = UserProfile


@register(User, site=admin_site)
class UserModelAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser')}),
    )

    inlines = [UserProfileInline]
