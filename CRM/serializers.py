from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.utils.translation import gettext_lazy as _

from authentication.models import CRMUser
from .models import Client, Contract, Event


def check_field(data: dict, key: str) -> bool:
    """check if a field exist and is not null"""
    return key in data and data[key] is not None and data[key] != ''


class EpicEventModelSerializer(ModelSerializer):
    # assignee = serializers.SlugRelatedField(queryset=CRMUser.objects.all(),
    #                                         slug_field='full_name')
    pass


class WriteClientSerializer(EpicEventModelSerializer):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name',
                  'email', 'phone', 'mobile', 'company')

    def validate(self, data):
        """
        Check phone, mobile or email have been entered
        """
        if not check_field(data, 'email') and not check_field(data, 'phone') \
                and not check_field(data, 'mobile'):
            raise serializers.ValidationError(_("You must record "
                                                "at least a phone, "
                                                "a mobile or an email"),
                                              code=400)
        return data


class ClientSerializer(EpicEventModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ContractSerializer(EpicEventModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        validated_data['assignee'] = self.context['user']
        # validated_data['issue'] = self.context['issue']
        return super().create(validated_data)

    # def validate(self, data):
    #     """check that a contract have a payment_due only once signed"""
    #     if data['status'] == Contract.Status.SIGNED \
    #             and check_field(data, 'payment_due') is None:
    #         raise serializers.ValidationError(
    #             _('When a contact is signed,'
    #               ' you have to determine a date of payment.'))
    #     if data['status'] != Contract.Status.SIGNED \
    #             and check_field(data, 'payment_due') is not None:
    #         raise serializers.ValidationError(
    #             _('You can determine a date of payment,'
    #               'if contract have not been signed.'))


class EventSerializer(EpicEventModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
