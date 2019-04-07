from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class ContactData(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
	object_id = models.PositiveIntegerField(blank=True, null=True)
	content_object = GenericForeignKey()

	phone = models.CharField(max_length=25,blank=True, null=True)
	email = models.EmailField()


class Person(models.Model):
    name = models.CharField(max_length=50)

    contact_data = GenericRelation(ContactData, related_query_name='content_obj_person')


class Skill(models.Model):
	name = models.CharField(max_length=50)
	person = models.ForeignKey('Person', related_name='skills', on_delete=models.CASCADE)

    # # address_data = JSONField(default=dict, blank=True)
    # address_data = GenericRelation(AddressData, related_query_name='content_obj_candidate')