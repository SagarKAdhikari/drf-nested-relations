from rest_framework import serializers
from nested_relations.decorators import helper_data_add, helper_data_update_with_delete
from nested_relations.serializers import NestedDataSerializer
from .models import ContactData, Person, Skill

class ContactDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactData
        exclude = ('content_type', 'object_id')

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ('person',)

class PersonSerializer(NestedDataSerializer, serializers.ModelSerializer):

    contact_data = serializers.JSONField(required=False, allow_null=True)
    skills = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = Person
        fields = '__all__'
        nestedSerializer = {
            'contact_data': {'serializer_class': ContactDataSerializer, 'many': True},
            'skills':{'serializer_class': SkillSerializer, 'many': True, 'type': 'fk', 'kwargs': 'person'}
        }

    @helper_data_add
    def create(self, validated_data):
        return super().create(validated_data)

    @helper_data_update_with_delete
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)