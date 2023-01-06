from django.contrib import admin
from epic_events.admin import admin_site
from django.contrib.auth.admin import UserAdmin

from authentication.models import CRMUser

admin.site.register(CRMUser)


@admin.register(CRMUser, site=admin_site)
class AdminUser(UserAdmin):
    list_display = ('full_name', 'group', 'assignments')
    list_filter = ("groups",)

    def full_name(self, obj):
        return str(obj)

    full_name.admin_order_field = 'last_name'

    # override to remove is_staff and is_superuser
    # that should not been accessible to management
    fieldsets = (
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'team')
        }),
        ('Permissions', {
            'fields': ('is_active',),
        }),
        ('Connexion', {'fields': ('username', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2', 'team')}),
    )
