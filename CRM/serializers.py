from datetime import date

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from django.utils.translation import gettext_lazy as _

from authentication.models import CRMUser
from .models import Client, Contract, Event


def check_field(data: dict, key: str) -> bool:
    """check if a field exist and is not null"""
    return key in data and data[key] is not None and data[key] != ''


class EpicEventModelSerializer(ModelSerializer):
    assignee = serializers.SlugRelatedField(
        read_only=True,
        slug_field='full_name'
    )


class DetailClientSerializer(EpicEventModelSerializer):
    next_event = SerializerMethodField(read_only=True)

    class Meta:
        model = Client
        fields = ('id',
                  'assignee',
                  'created_time',
                  'last_update',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'mobile',
                  'company',
                  'contract_set',
                  'next_event')

    def get_next_event(self, obj):
        result = None
        for contract in obj.contract_set.all():
            if hasattr(contract, 'event'):
                if contract.event.date >= date.today():
                    if result is None:
                        result = contract.event.date
                    else:
                        result = min(contract.event.date, result)

        return result or "No event scheduled"


class ListClientSerializer(DetailClientSerializer):
    class Meta:
        model = Client
        fields = ('id',
                  'first_name',
                  'last_name',
                  'company',
                  'assignee',
                  'next_event')


class ClientSerializer(EpicEventModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        validated_data['assignee'] = self.context['user']
        return super().create(validated_data)

    def validate(self, data):
        """Raise exception if no mobile, phone or mail have been furnished"""
        if self.instance is not None:
            if 'mobile' not in data:
                data['mobile'] = self.instance.mobile
            if 'phone' not in data:
                data['phone'] = self.instance.phone
            if 'email' not in data:
                data['email'] = self.instance.email

        if not any([check_field(data, field)
                    for field in ['email', 'phone', 'mobile']]):
            raise serializers.ValidationError(
                _('Each client must have a email, a phone or a mobile '))

        return data


class DetailContractSerializer(EpicEventModelSerializer):
    event = SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    client = serializers.SlugRelatedField(
        read_only=True,
        slug_field='company'
    )

    class Meta:
        model = Contract
        fields = ('id',
                  'assignee',
                  'client',
                  'created_time',
                  'last_update',
                  'status',
                  'amount',
                  'payment_due',
                  'event')

    def get_event(self, obj):
        if hasattr(obj, 'event'):
            return obj.event.date
        else:
            return None


class ListContractSerializer(EpicEventModelSerializer):
    status = serializers.CharField(source='get_status_display')
    client = serializers.SlugRelatedField(
        read_only=True,
        slug_field='company'
    )

    class Meta:
        model = Contract
        fields = ('id', 'assignee', 'client', 'status', 'amount')


class ContractSerializer(EpicEventModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'

    def validate(self, data):
        """add assignee on contract depending on assignee on client,
        checks that a contract have a payment_due only once signed"""
        if check_field(data, 'client'):
            # user is in context for creation, if there is no user, it's update
            # it's forbidden to update a contract, changing client
            if 'user' not in self.context:
                raise serializers.ValidationError(
                    _('You can\'t change client name on a contract '))
            if data['client'].assignee != self.context['user']:
                raise serializers.ValidationError(
                    _('You can\'t create a contract '
                      ' for clients of your colleagues.'))

        if not check_field(data, 'assignee'):
            if self.instance is not None:
                data['assignee'] = self.instance.assignee
            else:
                data['assignee'] = data['client'].assignee

        """ to validate in partial update"""
        if self.instance is not None:
            if 'status' not in data:
                data['status'] = self.instance.status
            if 'payment_due' not in data:
                data['payment_due'] = self.instance.payment_due

        if 'status' in data and data['status'] == Contract.Status.SIGNED \
                and not check_field(data, 'payment_due'):
            raise serializers.ValidationError(
                _('When a contact is signed,'
                  ' you have to determine a date of payment.'))
        if ('status' not in data or data['status'] != Contract.Status.SIGNED) \
                and check_field(data, 'payment_due'):
            raise serializers.ValidationError(
                _('You can\'t determine a date of payment,'
                  'if contract have not been signed.'))
        return data


class DetailEventSerializer(EpicEventModelSerializer):
    status = serializers.CharField(source='get_status_display')
    client = SerializerMethodField()

    class Meta:
        model = Event
        fields = ('contract',
                  'client',
                  'assignee',
                  'status',
                  'attendees',
                  'date',
                  'notes',
                  'created_time',
                  'last_update',)

    def get_client(self, obj):
        return obj.contract.client.company


class ListEventSerializer(EpicEventModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Event
        fields = ('contract', 'assignee', 'status', 'date')


class EventSerializer(EpicEventModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Event
        fields = '__all__'
