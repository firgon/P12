from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class ClientConfirmedListFilter(admin.SimpleListFilter):
    """filter confirmed client and potential client"""
    title = _('Status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'client_status'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('potential', _('Potential')),
            ('confirmed', _('Confirmed')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'potential':
            return queryset.filter(
                contract__isnull=True,
            )
        if self.value() == 'confirmed':
            return queryset.distinct().filter(
                contract__gt=0,
            )
