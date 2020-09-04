# Create your views here.

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import *
from .serializers import *

from flowable_rest.flowable_rest import FlowableRest

FR = FlowableRest()

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 1000


# ViewSets define the view behavior.
class FlowDefinitionViewSet(viewsets.ModelViewSet):
    queryset = FlowDefinition.objects.all()
    serializer_class = FlowDefinitionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        uuid = self.request.query_params.get('uuid', None)
        if uuid is not None:
            queryset = self.queryset.filter(uuid=uuid)
            return queryset
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        """
        增加一条信息
        """
        result =  FlowDefinition.objects.create(**request.data)
        return Response(data=result)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='list')
    def service(self, request, *args, **kwargs):
        """
        list service
        """
        queryset = self.queryset.filter(status='online')
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



# ViewSets define the view behavior.
class FlowCategpryViewSet(viewsets.ModelViewSet):
    queryset = FlowCategory.objects.all()
    serializer_class = FlowCategorySerializer
    pagination_class = None


# ViewSets define the view behavior.
class BPMNViewSet(viewsets.ModelViewSet):
    queryset = BPMN.objects.all()
    serializer_class = BPMNSerializer
    pagination_class = None

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        flow_uid = self.request.query_params.get('flow_uid', None)
        if id is not None and flow_uid is not None:
            queryset = self.queryset.filter(id=id, flow_uid=flow_uid)
            return queryset
        if id is not None:
            queryset = self.queryset.filter(id=id)
            return queryset
        return super().get_queryset()

    @action(methods=['POST'], detail=True)
    def start(self, request, *args, **kwargs):
        """
        start a process instance.
        """
        pk = kwargs['pk']
        status_code, text = FR.launchProcessInstance(pk=pk)
        return Response(data=text, status=status_code)

# ViewSets define the view behavior.
class FlowInstanceViewSet(viewsets.ModelViewSet):
    queryset = FlowInstance.objects.all()
    serializer_class = FlowInstanceSerializer
    pagination_class = StandardResultsSetPagination


class TaskInstanceViewSet(viewsets.ModelViewSet):
    queryset = TaskInstance.objects.all()
    serializer_class = TaskInstanceSerializer
    pagination_class = StandardResultsSetPagination