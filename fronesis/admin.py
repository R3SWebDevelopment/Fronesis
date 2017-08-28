from django.contrib.admin import AdminSite
from django.contrib.admin import register
from django.contrib.sites.models import Site
from django.contrib import admin


class CustomAdminSite(AdminSite):
    site_header = 'Fronesis'



admin_site = CustomAdminSite(name='fronesis')

@register(Site, site=admin_site)
class KeywordModelAdmin(admin.ModelAdmin):
    pass
