
from datetime import datetime

from django.db import models
from django.utils import timezone

'''
flowable model:
deployment -> processDefinition -> processInstance -> taskInstance

lipotes model:
flow_definition -> bpmn_version -> 
'''


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

    uid = models.CharField(max_length=64, unique=True,)
    uname = models.CharField(max_length=32, unique=True)
    category = models.CharField(max_length=32)
    bpmn_uid = models.CharField(max_length=64)
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
        verbose_name = 'flow_definition'
        # 复数名
        verbose_name_plural = '流程定义'
        ordering = ['-id']


class FlowCategory(models.Model):
    uid = models.CharField(max_length=64, unique=True)
    uname = models.CharField(max_length=32, unique=True)

    # 定义model的元数据
    class Meta:
        # 数据库中的表名称
        db_table = "flow_category"
        # 单数名
        verbose_name = 'flow_category'
        # 复数名
        verbose_name_plural = '流程分类定义，便于维护'
        ordering = ['-id']


class BPMN(models.Model):
    uid = models.CharField(max_length=64, unique=True)
    flow_uid = models.CharField(max_length=64)
    version = models.CharField(max_length=32)
    content = models.TextField()
    # flowable_process_definition_id
    flowable_id = models.CharField(max_length=64, null=True, unique=True)

    # 定义model的元数据
    class Meta:
        # 数据库中的表名称
        db_table = "flow_bpmn"
        # 数据库表名
        verbose_name = 'flow_bpmn'
        # human readable
        verbose_name_plural = 'flow_bpmns'
        ordering = ['-id']


class FlowInstance(models.Model):
    uid = models.CharField(max_length=64, unique=True)
    # flowable_instance_id
    flowable_id = models.CharField(max_length=64, unique=True)
    start_user_id = models.CharField(max_length=32)
    # 保持和flowable时间一致
    start_time = models.DateTimeField(auto_now_add=False, help_text='创建时间')
    # 可以对应到flowable_process_definition_id
    bpmn_uid = models.CharField(max_length=64)
    

    # 定义model的元数据
    class Meta:
        # 数据库中的表名称
        db_table = "flow_instance"
        # 数据库表名
        verbose_name = 'flow_instance'
        # human readable
        verbose_name_plural = 'flow_instances'
        ordering = ['-id']