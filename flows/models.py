
import uuid
from datetime import datetime

from django.db import models
from django.utils import timezone

'''
flowable model:
deployment -> processDefinition -> processInstance -> taskInstance

lipotes model:
flow -> flow_bpmn -> flow_instance -> task_instance
     -> flow_category
'''

FLOWBPMN_STATUS_CHOICES = (
        ('draft', '草稿',),
        ('deployed', '已部署',),
        ('del', '删除',),
    )

TASKINSTANCE_STATUS_CHOICES = (
        ('running', '进行中',),
        ('completed', '已完成',),
        ('rejected', '已拒绝',),
        ('cancled', '已撤回',),
    )

def genTagNum():
    fmt = '%y%m%d%H%M%S'
    return datetime.now().strftime(fmt)

def genOrderNum(prefix=''):
    return prefix + genTagNum()

class Base(models.Model):
    uuid = models.CharField(verbose_name="UUID", max_length=64, default=uuid.uuid1, editable=False, unique=True)
    ctime = models.DateTimeField(auto_now_add=True, help_text='创建时间', blank=True, null=True)
    mtime = models.DateTimeField(auto_now=True, help_text='修改时间', blank=True, null=True)
    
    class Meta:
        abstract=True


class Flow(Base):
    # FlowBaseInfo
    name = models.CharField(max_length=32, unique=True)
    category = models.ForeignKey('FlowCategory', to_field='uuid', null=True, blank=True, on_delete=models.PROTECT, related_name='flows') # CASCADE 主表的字段删除时，和它有关的子表字段也删除
    bpmn = models.ForeignKey('FlowBpmn', to_field='uuid', null=True, blank=True, on_delete=models.PROTECT, related_name='flows')
    # 自定义字段
    extend_fields = models.TextField(default={})

    #   定义model的元数据,在admin中显示
    class Meta:
        # 数据库中的表名称
        db_table = "flow"
        # 单数名
        verbose_name = 'flows'
        # 复数名
        verbose_name_plural = '流程定义'
        ordering = ['-id']


class FlowBpmn(Base):
    # FlowVersion
    tag = models.CharField(max_length=32, default=genTagNum, editable=False)
    content = models.TextField()
    flow = models.ForeignKey('Flow', to_field='uuid', null=True, blank=True, on_delete=models.PROTECT, related_name='related_flow')
    flowable_process_definition_id = models.CharField(max_length=64, null=True, unique=True, blank=True)
    status = models.CharField(max_length=16, default='draft', choices=FLOWBPMN_STATUS_CHOICES)

    # 定义model的元数据
    class Meta:
        # 数据库中的表名称
        db_table = "flow_bpmn"
        # 数据库表名
        verbose_name = 'flow_bpmn'
        # human readable
        verbose_name_plural = 'flow_bpmns'
        ordering = ['-id']


class FlowCategory(Base):

    name = models.CharField(max_length=32, unique=True)
    # 定义model的元数据
    class Meta:
        # 数据库中的表名称
        db_table = "flow_category"
        # 单数名
        verbose_name = 'flow_category'
        # 复数名
        verbose_name_plural = 'flow_categories'
        ordering = ['-id']


class FlowInstance(Base):
    completed = models.BooleanField(default=False)
    # 工单名称，发起时填写
    name = models.CharField(max_length=64)
    num = models.CharField(default=genOrderNum, max_length=32, editable=False)
    flowable_process_instance_id = models.CharField(max_length=64, unique=True)
    start_user_id = models.CharField(max_length=32)
    # 保持和flowable时间一致
    start_time = models.DateTimeField(auto_now_add=False, help_text='创建时间')
    flow_bpmn = models.ForeignKey('FlowBpmn', to_field='uuid', null=True, blank=True, on_delete=models.PROTECT, related_name='related_bpmn')
    
    # 定义model的元数据
    class Meta:
        # 数据库中的表名称
        db_table = "flow_instance"
        # 数据库表名
        verbose_name = 'flow_instance'
        # human readable
        verbose_name_plural = 'flow_instances'
        ordering = ['-id']


class TaskInstance(Base):
    status = models.CharField(max_length=16, default='running', choices=TASKINSTANCE_STATUS_CHOICES)
    # flowable process instance id
    flowable_process_instance_id = models.CharField(max_length=64, null=True)
    # flowable_task_instance_id
    flowable_task_instance_id = models.CharField(max_length=64, unique=True)
    task_definition_key = models.CharField(max_length=32)
    # 节点名称
    name = models.CharField(max_length=32)
    # 同步flowable的创建时间
    flowable_created_time = models.DateTimeField()
    flow_instance = models.ForeignKey('FlowInstance', to_field='uuid', null=True, blank=True, on_delete=models.PROTECT, related_name='related_flow_instance')

    # 定义model的元数据
    class Meta:
        db_table = "task_instance"
        verbose_name = "task_instance"
        # human readable
        verbose_name_plural = 'task_instances'
        ordering = ['-id']
