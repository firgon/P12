from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from itertools import chain

from CRM.models import Client, Contract, Event
from CRM.permissions import IsRelatedOrReadOnly
from CRM.serializers import ClientSerializer, ContractSerializer, \
    EventSerializer, DetailClientSerializer, ListClientSerializer, \
    DetailContractSerializer, ListContractSerializer, DetailEventSerializer, \
    ListEventSerializer


class GeneralViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, `update` and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {'assignee': ['exact', 'isnull']}
    permission_classes = [IsAuthenticated,
                          IsRelatedOrReadOnly,
                          DjangoModelPermissions]

    def get_serializer_class(self):
        # return list serializer if list asked
        if self.action == 'retrieve':
            return self.detail_serializer_class
        if self.action == 'list':
            return self.list_serializer_class
        else:
            return super().get_serializer_class()

    def create(self, *args, **kwargs):
        """override method to check form data"""
        serializer = self.serializer_class(data=self.request.data,
                                           context={'user': self.request.user},
                                           partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ClientViewSet(GeneralViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    detail_serializer_class = DetailClientSerializer
    list_serializer_class = ListClientSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {'assignee': ['exact', 'isnull'],
                        'company': ['exact']}
    permission_classes = [IsAuthenticated,
                          IsRelatedOrReadOnly,
                          DjangoModelPermissions]

#
# class MyClientViewSet(GeneralViewSet):
#     """set of view to see only client related to connected user"""
#     serializer_class = ClientSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Client.objects.all().filter(
#             Q(assignee=user) | Q(contract__assignee=user)
#             | Q(contract__event__assignee=user))
#         return queryset


class ContractViewSet(GeneralViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    detail_serializer_class = DetailContractSerializer
    list_serializer_class = ListContractSerializer
    permission_classes = [IsAuthenticated,
                          IsRelatedOrReadOnly,
                          DjangoModelPermissions]
    filterset_fields = {'assignee': ['exact', 'isnull'],
                        'status': ['exact'],
                        'client': ['exact']}


# class MyContractViewSet(GeneralViewSet):
#     """set of view to see only contracts related to connected user"""
#     serializer_class = ContractSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Contract.objects.all().filter(
#             Q(assignee=user) | Q(client__assignee=user)
#             | Q(event__assignee=user))
#         return queryset


class EventViewSet(GeneralViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    detail_serializer_class = DetailEventSerializer
    list_serializer_class = ListEventSerializer
    permission_classes = [IsAuthenticated,
                          IsRelatedOrReadOnly,
                          DjangoModelPermissions]
    filterset_fields = {'assignee': ['exact', 'isnull'],
                        'status': ['exact'],
                        'contract__client': ['exact']}




# class MyEventViewSet(GeneralViewSet):
#     """set of view to see only events related to connected user"""
#     serializer_class = EventSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Event.objects.all().filter(
#             Q(assignee=user) | Q(contract__assignee=user)
#             | Q(contract__client__assignee=user))
#         return queryset
#
#
# class AssignmentsToDo(APIView):
#     queryset = list(chain(Client.objects.all().filter(assignee__isnull=True),
#                           Event.objects.all().filter(assignee__isnull=True)))
