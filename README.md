
# DRF Nested Relations

This python package is an extension for django rest framework for  creating, updating and deleting nested relations. The nested relations can go to `any depth`.

It receives nested data as list of dictionaries. 
It works for generic relations and foreign keys for now.

Creating data is as usual (see section <b> Writing data </b>).

Updating data with its nested data which can go recursively to any depth (see section <b> Writing data </b>) :
* If the dictionary contains `id` field, the corresponding nested data will be updated.

* If the dictionary does not contain `id`, field , new nested data will be created.

* If the dictionary contains only `id` as key, the nested data will be deleted.

There is no need to provide nested data which do not need to be updated or deleted.

# Installation

1. Install the package from pypi using pip:

    `pip install drf-nested-relations`

2. Add `nested_relations` to INSTALLED_APPS.
    ```python
    
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',  # utilities for rest apis

    # drf nested relations
    'nested_relations',
   ]```


# Usage

### Models 

```python
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

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
````

### Serializers

```Python
from rest_framework import serializers
from nested_relations.serializers import NestedDataModelSerializer
from .models import ContactData, Person, Skill

class ContactDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactData
        exclude = ('content_type', 'object_id')

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ('person',)

class PersonSerializer(NestedDataModelSerializer):

    contact_data = serializers.JSONField(required=False, allow_null=True)
    skills = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = Person
        fields = '__all__'
        nestedSerializer = {
            'contact_data': {'serializer_class': ContactDataSerializer, 'many': True, 'kwargs': 'content_object'},
            'skills':{'serializer_class': SkillSerializer, 'many': True, 'kwargs': 'person'}
        }

   
```


* For generic relation , 
use `field_name = serializers.JSONField()`  and same `field_name` in nested serializer. (An attribute in main model that points to nested relation)

* For foreign key, 
Use `related_name = serializers.JSONField()` and same `related_name` in nested serializer. (An attribute in main model that points to nested relation)

* For both,
Provide `many=True`. The value for `kwargs` is clear from example. It is an attribute in nested relation that points to main model.

## Writing data
```python
# Creating a person

data = {
    "contact_data": [{"email":"1@1.com"},{"email":"2@2.com"}, {"email":"3@3.com"}],
    "name": "Sagar"
}

person_serializer = PersonSerializer(data=data,  context={'request':request})
person_serializer.is_valid(raise_exception=True)
person = person_serializer.save()
print(person_serializer.data)

{
    "id": 3,
    "contact_data": [
        {
            "id": 4,
            "phone": null,
            "email": "1@1.com"
        },
        {
            "id": 5,
            "phone": null,
            "email": "2@2.com"
        },
        {
            "id": 6,
            "phone": null,
            "email": "3@3.com"
        }
    ],
    "skills": [],
    "name": "Sagar"
}

# Updating the person
data = {
    "id": 3,
    "contact_data": [
        {   # update
            "id": 4,  
            "phone": null,
            "email": "1@1edit.com"
        },
        {   # delete
            "id": 5    
        },
        {   # create        
            "phone": null, 
            "email": "4@4.com"
        }
    ],
    "skills": [],
    "name": "Sagar"
}

person_serializer = PersonSerializer(person, data=data, context={'request':request})
person_serializer.save()
print(person_serializer.data)

{
    "id": 3,
    "contact_data": [
        {
            "id": 4,
            "phone": null,
            "email": "1@1edit.com"
        },
        {   # no change
            "id": 6,
            "phone": null,
            "email": "3@3.com" 
        },
        {
            "id": 7,
            "phone": null,
            "email": "4@4.com"
        }
    ],
    "skills": [],
    "name": "Sagar"
}
```
## Deeper Relations
For deeper relations, the nested serializer should further inherit `NestedDataModelSerializer` and their corresponding nested serializers have to be provided in the similar manner as shown.


