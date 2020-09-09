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
class FlowViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializerReadOnly
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        uuid = self.request.query_params.get('uuid', None)
        if uuid is not None:
            queryset = self.queryset.filter(uuid=uuid) # objects 的 get 唯一匹配
            return queryset
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        """
        增加一条信息
        """
        result =  Flow.objects.create(**request.data)
        return Response(data=result)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # 此处区分请求的HTTP1.1方法
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method in ('PUT', 'PATCH', 'POST'):
            serializer_class = FlowSerializerWritable
        if self.request.method == 'GET':
            serializer_class = FlowSerializerReadOnly
        return serializer_class

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
        # queryset = self.queryset.filter(bpmn__flowable_process_definition_id__isnull=False)
        queryset = self.queryset.filter(bpmn__status__exact='deployed')
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
    pagination_class = StandardResultsSetPagination


# ViewSets define the view behavior.
class FlowBpmnViewSet(viewsets.ModelViewSet):
    queryset = FlowBpmn.objects.all()
    serializer_class = FlowBpmnSerializerReadOnly
    pagination_class = StandardResultsSetPagination

    # 此处区分请求的HTTP1.1方法
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method in ('PUT', 'PATCH', 'POST'):
            serializer_class = FlowBpmnSerializerWritable
        if self.request.method == 'GET':
            serializer_class = FlowBpmnSerializerReadOnly
        return serializer_class

    def get_queryset(self):
        # flow_uuid
        flow = self.request.query_params.get('flow', None)
        if flow is not None:
            queryset = self.queryset.filter(flow=flow)
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
    serializer_class = FlowInstanceSerializerReadOnly
    pagination_class = StandardResultsSetPagination
    
    # 此处区分请求的HTTP1.1方法
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method in ('PUT', 'PATCH', 'POST'):
            serializer_class = FlowInstanceSerializerWritable
        if self.request.method == 'GET':
            serializer_class = FlowInstanceSerializerReadOnly
        return serializer_class

class TaskInstanceViewSet(viewsets.ModelViewSet):
    queryset = TaskInstance.objects.all()
    serializer_class = TaskInstanceSerializer
    pagination_class = StandardResultsSetPagination