# Create your views here.

from django.shortcuts import render
from rest_framework import serializers, viewsets, pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import *


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'limit'
    max_page_size = 1000


# Serializers define the API representation.
class FlowDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FlowDefinition
        fields = ['id', 'uniq_key', 'uniq_name', 'category', 'online_bpmn_key', 'status']


# Serializers define the API representation.
class FlowCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FlowCategory
        fields = ['id', 'uniq_key', 'annotation']


# Serializers define the API representation.
class BPMN20XMLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BPMN20XML
        fields = ['id', 'uniq_key', 'flow_uniq_key', 'bpmn_content', 'version']


# ViewSets define the view behavior.
class FlowDefinitionViewSet(viewsets.ModelViewSet):
    queryset = FlowDefinition.objects.all()
    serializer_class = FlowDefinitionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        pkey = self.request.query_params.get('uniq_key', None)
        if pkey is not None:
            queryset = self.queryset.filter(uniq_key=pkey)
            return queryset
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        """
        增加一条信息
        """
        print(request.data)
        result =  FlowDefinition.objects.create(**request.data)
        return Response(data=result)


# ViewSets define the view behavior.
class FlowCategpryViewSet(viewsets.ModelViewSet):
    queryset = FlowCategory.objects.all()
    serializer_class = FlowCategorySerializer
    pagination_class = None


# ViewSets define the view behavior.
class BPMN20XMLViewSet(viewsets.ModelViewSet):
    queryset = BPMN20XML.objects.all()
    serializer_class = BPMN20XMLSerializer
    pagination_class = None

    def get_queryset(self):
        uniq_key = self.request.query_params.get('uniq_key', None)
        flow_uniq_key = self.request.query_params.get('flow_uniq_key', None)
        if uniq_key and flow_uniq_key:
            queryset = self.queryset.filter(uniq_key=uniq_key, flow_uniq_key=flow_uniq_key)
            return queryset
        return super().get_queryset()

