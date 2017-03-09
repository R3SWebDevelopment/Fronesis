from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.admin import register, TabularInline
from django.contrib.auth.models import User, Group
from fronesis.admin import admin_site
from .models import UserProfile


class UserProfileInline(TabularInline):
    model = UserProfile
    max_num = 1
    min_num = 1


@register(User, site=admin_site)
class UserModelAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups')}),
    )

    inlines = [UserProfileInline]


@register(Group, site=admin_site)
class GroupModelAdmin(GroupAdmin):
    pass
