# Create your views here.

from django.shortcuts import render
from rest_framework import serializers, viewsets

from .models import ProcessDefinition

# Serializers define the API representation.
class ProcessDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProcessDefinition
        fields = ['pkey', 'pname', 'version', 'bpmn2']


# ViewSets define the view behavior.
class ProcessDefinitionViewSet(viewsets.ModelViewSet):
    queryset = ProcessDefinition.objects.all()
    serializer_class = ProcessDefinitionSerializer

