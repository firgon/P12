from rest_framework.serializers import ModelSerializer

from .models import Client, Contract, Event


class ClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


class ContractSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'


class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


# class ProjectDetailSerializer(ModelSerializer):
#     issues = PrimaryKeyRelatedField(many=True, read_only=True)
#
#     class Meta:
#         model = Project
#         fields = '__all__'
#
#     def create(self, validated_data):
#         instance: Project = super().create(validated_data)
#         user = self.context['request'].user
#         instance.add_contributor(user, role=Contributor.Role.author)
#         return instance
