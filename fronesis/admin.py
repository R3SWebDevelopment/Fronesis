from django.contrib.admin import AdminSite, register
from django.utils.translation import gettext_lazy as _

from mezzanine.generic.admin import ThreadedCommentAdmin
from drum.links.admin import LinkAdmin, KeywordAdmin
from django.contrib.auth.admin import UserAdmin

from mezzanine.generic.models import ThreadedComment
from mezzanine.generic.models import Keyword
from django.contrib.auth.models import User
from drum.links.models import Link


class CustomAdminSite(AdminSite):
    site_header = 'Fronesis'


admin_site = CustomAdminSite(name='fronesis')


@register(User, site=admin_site)
class UserModelAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser')}),
    )


@register(Link, site=admin_site)
class LinkModelAdmin(LinkAdmin):
    pass


@register(Keyword, site=admin_site)
class KeywordModelAdmin(KeywordAdmin):
    pass


@register(ThreadedComment, site=admin_site)
class ThreadedCommentModelAdmin(ThreadedCommentAdmin):
    pass
