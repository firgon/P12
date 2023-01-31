from django.forms import ModelForm

from CRM.models import Contract, Event


class AddContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = [
            'client',
            'amount',
            'status',
            'payment_due'
        ]
        help_texts = {
            'client': 'Client must have a sales assignee',
        }


class ChangeEventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'assignee',
            'attendees',
            'date',
            'notes'
        ]
