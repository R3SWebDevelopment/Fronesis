from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = 'Fronesis'


admin_site = CustomAdminSite(name='fronesis')
