# Create your views here.
import json

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from flows.models import *
from flows.serializers import *
from flowable_rest.flowable_rest import FR
from flows.signals import post_flowable_task_action


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
    serializer_class = TaskInstanceSerializerReadOnly
    pagination_class = StandardResultsSetPagination
    serializer_class_writable = TaskInstanceSerializerWritable

    def get_queryset(self):
        # task_uuid
        uuid = self.request.query_params.get('uuid', None)
        if uuid is not None:
            queryset = self.queryset.filter(uuid=uuid)
            return queryset
        
        status =  self.request.query_params.get('status', None)
        if status is not None:
            queryset = self.queryset.filter(status=status)
            return queryset
        return super().get_queryset()
    
    # 此处区分请求的HTTP1.1方法
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method in ('PUT', 'PATCH', 'POST'):
            serializer_class = self.serializer_class_writable
        if self.request.method == 'GET':
            serializer_class = self.serializer_class
        return serializer_class
    
    @action(methods=['POST'], detail=True)
    def complete(self, request, *args, **kwargs):
        """
        excute a task instance action.
        """
        flowable_task_id = kwargs['pk']
        task_instance = self.queryset.get(flowable_task_instance_id=flowable_task_id)
        if task_instance.status == 'completed':
            return Response(data='任务已完成，无须重复操作', status=500)

        data = {"action": "complete"}
        uri = '/runtime/tasks/{}'.format(flowable_task_id)
        resp = FR.request(uri=uri, method='post', data=data)
        if resp.status_code!=200:
            resp_data = resp.text
            return Response(data=resp_data if resp_data else 'complete flowable task error', status=resp.status_code)
        
        # 将第一个任务状态改为comleted
        task_instance.status = 'completed'
        task_instance.__dict__.update(task_instance.__dict__)
        task_instance.save()
        post_flowable_task_action.send_robust(sender='flows.TaskInstance', instance=task_instance, raw='', created=True)
        resp_data = resp.text
        return Response(data=resp_data if resp_data else 'action done', status=resp.status_code)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializerReadOnly
    pagination_class = StandardResultsSetPagination
    serializer_class_writable = TaskSerializerWritable

    def get_queryset(self):
        flow_bpmn = self.request.query_params.get('flow_bpmn', None)
        if flow_bpmn is not None:
            queryset = self.queryset.filter(flow_bpmn=flow_bpmn)
            return queryset
        return super().get_queryset()

    # 此处区分请求的HTTP1.1方法
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method in ('PUT', 'PATCH', 'POST'):
            serializer_class = self.serializer_class_writable
        if self.request.method == 'GET':
            serializer_class = self.serializer_class
        return serializer_class

class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializerReadOnly
    pagination_class = StandardResultsSetPagination
    serializer_class_writable = FormSerializerWritable

    def get_queryset(self):
        uuid = self.request.query_params.get('uuid', None)
        if uuid is not None:
            queryset = self.queryset.filter(uuid=uuid)
            return queryset
        return super().get_queryset()

    # 此处区分请求的HTTP1.1方法
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method in ('PUT', 'PATCH', 'POST'):
            serializer_class = self.serializer_class_writable
        if self.request.method == 'GET':
            serializer_class = self.serializer_class
        return serializer_class

class FormContentViewSet(viewsets.ModelViewSet):
    queryset = FormContent.objects.all()
    serializer_class = FormContentSerializerReadOnly
    pagination_class = StandardResultsSetPagination
    serializer_class_writable = FormContentSerializerWritable

    def get_queryset(self):
        form = self.request.query_params.get('form', None)
        if form is not None:
            queryset = self.queryset.filter(form=form)
            return queryset
        return super().get_queryset()

    # 此处区分请求的HTTP1.1方法
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method in ('PUT', 'PATCH', 'POST'):
            serializer_class = self.serializer_class_writable
        if self.request.method == 'GET':
            serializer_class = self.serializer_class
        return serializer_class
