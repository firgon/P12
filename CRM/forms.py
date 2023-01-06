from django.forms import ModelForm

from CRM.models import Contract, Event


class AddContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = [
            'client',
            'amount',
            'payment_due'
        ]
        help_texts = {
            'client': 'Client must have a sales assignee',
        }


class AddEventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'contract',
            'assignee',
            'attendees',
            'date',
            'notes'
        ]
        help_texts = {
            'contract': 'Contract must have been signed and have no event yet',
        }
