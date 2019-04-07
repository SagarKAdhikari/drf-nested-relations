from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Person
from .serializers import PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):

	serializer_class = PersonSerializer

	queryset = Person.objects.all()