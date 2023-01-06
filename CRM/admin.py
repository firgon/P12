from django.contrib import admin
from django.contrib.admin import ModelAdmin

from CRM.filters import ClientConfirmedListFilter
from CRM.forms import AddContractForm, AddEventForm
from CRM.models import Contract, Event, Client
from epic_events.admin import admin_site

admin.site.register(Contract)
admin.site.register(Client)
admin.site.register(Event)


@admin.register(Client, site=admin_site)
class AdminClient(ModelAdmin):
    list_display = ('full_name', 'status', 'assignee')
    list_filter = ('assignee', ClientConfirmedListFilter)
    empty_value_display = 'To Assign !!!'
    list_display_links = ('full_name', 'assignee')

    def full_name(self, obj):
        return str(obj)

    def status(self, obj):
        return 'Confirmed' if obj.is_confirmed else 'Potential'

    full_name.admin_order_field = 'last_name'
    full_name.short_description = 'client'


@admin.register(Contract, site=admin_site)
class AdminContract(ModelAdmin):
    list_display = ('contract', 'assignee', 'payment_due', 'status')
    list_filter = ('status', 'payment_due', 'client')
    list_display_links = ('contract', 'status')
    add_form = AddContractForm

    def contract(self, obj):
        return str(obj)

    contract.admin_order_field = 'id'

    def get_form(self, request, obj=None, change=False, **kwargs):
        """use custom Form when adding new contract"""
        default = {}
        if obj is None:
            default['form'] = self.add_form
        default.update(**kwargs)
        return super().get_form(request, obj, change, **default)


@admin.register(Event, site=admin_site)
class AdminEvent(ModelAdmin):
    list_display = ('event', 'assignee', 'status')
    list_filter = ('status', 'assignee', 'contract__client')

    empty_value_display = 'To Assign !!!'
    list_display_links = ('event', 'assignee',)
    add_form = AddEventForm

    def event(self, obj):
        return str(obj)

    event.admin_order_field = 'date'
    event.short_description = 'Event'

    def get_form(self, request, obj=None, change=False, **kwargs):
        """use custom Form when adding new contract"""
        default = {}
        if obj is None:
            default['form'] = self.add_form
        default.update(**kwargs)
        return super().get_form(request, obj, change, **default)

    def __str__(self):
        return f"{self.date}-{self.client()}"
