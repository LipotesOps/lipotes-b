
import uuid
from datetime import datetime

from django.db import models
from django.utils import timezone

'''
flowable model:
deployment -> processDefinition -> processInstance -> taskInstance

lipotes model:
flow_definition -> bpmn_version -> 
'''

def generateTagNum():
    now = datetime.now()
    year = str(now.year-2000)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    min = str(now.minute)
    sec = str(now.second)

    str_time = ''.join([year,month,day,hour,min,sec])
    return str_time
    

class Base(models.Model):
    uuid = models.CharField(verbose_name="UUID", max_length=64, default=uuid.uuid1, editable=False, unique=True)
    ctime = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    mtime = models.DateTimeField(auto_now=True, help_text='修改时间')
    
    class Meta:
        abstract=True


class Flow(Base):
    # FlowBaseInfo
    name = models.CharField(max_length=32, unique=True)
    category = models.ForeignKey('FlowCategory', to_field='uuid', null=True, blank=True, on_delete=models.CASCADE, related_name='related_category') # 主表的字段删除时，和它有关的子表字段也删除
    bpmn = models.ForeignKey('FlowBpmn', to_field='uuid', null=True, blank=True, on_delete=models.CASCADE, related_name='related_bpmn')
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
    status_choices = (
        ('draft', '草稿',),
        ('online', '生效',),
        ('offline', '下线',),
        ('del', '删除',),
    )
    tag = models.CharField(max_length=32, default=generateTagNum, editable=False)
    content = models.TextField()
    flow = models.ForeignKey('Flow', to_field='uuid', null=True, blank=True, on_delete=models.CASCADE, related_name='related_flow')
    flowable_process_definition_id = models.CharField(max_length=64, null=True, unique=True, blank=True)
    status = models.CharField(max_length=32, default='draft', choices=status_choices)

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
    flowable_process_instance_id = models.CharField(max_length=64, unique=True)
    start_user_id = models.CharField(max_length=32)
    # 保持和flowable时间一致
    start_time = models.DateTimeField(auto_now_add=False, help_text='创建时间')
    
    # 定义model的元数据
    class Meta:
        # 数据库中的表名称
        db_table = "flow_instance"
        # 数据库表名
        verbose_name = 'flow_instance'
        # human readable
        verbose_name_plural = 'flow_instances'
        ordering = ['-id']


class TaskInstance(models.Model):
    # flowable_task_instance_id
    flowable_task_instance_id = models.CharField(max_length=64, unique=True)
    task_definition_key = models.CharField(max_length=32)
    # 节点名称
    name = models.CharField(max_length=32)
    # 同步flowable的创建时间
    create_time = models.DateTimeField()

    # 定义model的元数据
    class Meta:
        db_table = "task_instance"
        verbose_name = "task_instance"
        # human readable
        verbose_name_plural = 'task_instances'
        ordering = ['-id']
