
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

def generateVersionNum():
    now = datetime.now()
    year = now.year-2000
    month = now.month
    day = now.day
    hour = now.hour
    min = now.minute
    sec = now.second

    str_time = ''.join([year,month.day,hour,min,sec])
    return str_time
    

# 抽象model
class Human(models.Model):
    name=models.CharField(max_length=100)
    GENDER_CHOICE=((u'M',u'Male'),(u'F',u'Female'),)
    gender=models.CharField(max_length=2,choices=GENDER_CHOICE,null=True)
    class Meta:
        abstract=True

class FlowDefinition(models.Model):
    status_choices = {
        'draft': '草稿',
        'online': '生效',
        'offline': '下线',
        'del': '删除'
    }

    id = models.CharField(verbose_name="流程定义ID", max_length=64, primary_key=True, default=uuid.uuid1, editable=False, unique=True)
    uname = models.CharField(max_length=32, unique=True)
    category = models.CharField(max_length=32)
    version_id = models.CharField(verbose_name="流程定义版本ID", max_length=64)
    status = models.CharField(max_length=32, default='draft', choices=status_choices.items())
    # 自定义字段
    extend_fields = models.TextField(default={})
    ctime = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    mtime = models.DateTimeField(auto_now_add=True, help_text=u'修改时间')

    #   定义model的元数据,在admin中显示
    class Meta:
        # 数据库中的表名称
        db_table = "flow_definition"
        # 单数名
        verbose_name = 'flow_definitions'
        # 复数名
        verbose_name_plural = '流程定义'
        ordering = ['-id']


class FlowCategory(models.Model):
    id = models.CharField(verbose_name="流程分类ID", max_length=64, primary_key=True, default=uuid.uuid1, editable=False, unique=True)
    uname = models.CharField(max_length=32, unique=True)

    # 定义model的元数据
    class Meta:
        # 数据库中的表名称
        db_table = "flow_definition_category"
        # 单数名
        verbose_name = 'flow_definition_category'
        # 复数名
        verbose_name_plural = 'flow_definition_categories'
        ordering = ['-id']

# definiton with version
class BPMN(models.Model):
    id = models.CharField(verbose_name="流程定义bpmn版本ID", max_length=64, primary_key=True, default=uuid.uuid1, editable=False, unique=True)
    version = models.CharField(max_length=32, default=generateVersionNum, editable=False)
    content = models.TextField()
    flowable_process_definition_id = models.CharField(max_length=64, null=True, unique=True)

    # 定义model的元数据
    class Meta:
        # 数据库中的表名称
        db_table = "flow_definition_version"
        # 数据库表名
        verbose_name = 'flow_definition_version'
        # human readable
        verbose_name_plural = 'flow_definition_versions'
        ordering = ['-version']


class FlowInstance(models.Model):
    id = models.CharField(verbose_name="流程实例ID", max_length=64, primary_key=True, default=uuid.uuid1, editable=False, unique=True)
    flowable_process_instance_id = models.CharField(max_length=64, unique=True)
    start_user_id = models.CharField(max_length=32)
    # 保持和flowable时间一致
    start_time = models.DateTimeField(auto_now_add=False, help_text='创建时间')
    # 可以对应到flowable_process_definition_id
    definition_id = models.CharField(max_length=64)
    

    # 定义model的元数据
    class Meta:
        # 数据库中的表名称
        db_table = "flow_inst"
        # 数据库表名
        verbose_name = 'flow_instance'
        # human readable
        verbose_name_plural = 'flow_instances'
        ordering = ['-id']


class TaskInstance(models.Model):
    id = models.CharField(verbose_name="任务实例ID", max_length=64, primary_key=True, default=uuid.uuid1, editable=False, unique=True)
    # flowable_task_instance_id
    flowable_task_instance_id = models.CharField(max_length=64, unique=True)
    taskDefinitionKey = models.CharField(max_length=32)
    # 节点名称
    name = models.CharField(max_length=32)
    # 同步flowable的创建时间
    create_time = models.DateTimeField()

    # 定义model的元数据
    class Meta:
        db_table = "task_inst"
        verbose_name = "task_instance"
        # human readable
        verbose_name_plural = 'task_instances'
        ordering = ['-id']
