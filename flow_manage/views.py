# Create your views here.

from django.shortcuts import render
from rest_framework import serializers, viewsets, pagination
from rest_framework.pagination import PageNumberPagination

from .models import ProcessDefinition


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 10000

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'limit'
    max_page_size = 1000


# Serializers define the API representation.
class ProcessDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProcessDefinition
        fields = ['pkey', 'pname', 'version', 'bpmn2', 'status']


# ViewSets define the view behavior.
class ProcessDefinitionViewSet(viewsets.ModelViewSet):
    queryset = ProcessDefinition.objects.all()
    serializer_class = ProcessDefinitionSerializer
    pagination_class = StandardResultsSetPagination

