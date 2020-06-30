
from datetime import datetime

from django.db import models
from django.utils import timezone


class FlowDefinition(models.Model):
    status_choices = {
        'draft': '草稿',
        'online': '生效',
        'offline': '下线',
        'del': '删除'
    }

    uniq_key = models.CharField(max_length=32, unique=True,)
    uniq_name = models.CharField(max_length=32, unique=True)
    category = models.CharField(max_length=32)
    online_bpmn_key = models.CharField(max_length=32)
    status = models.CharField(max_length=32, default='draft', choices=status_choices.items())

    ctime = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    mtime = models.DateTimeField(auto_now_add=True, help_text=u'修改时间')

    #   定义model的元数据,在admin中显示
    class Meta:
        # 数据库表名
        verbose_name = 't_flow_definition'
        # human readable
        verbose_name_plural = '流程基本信息定义'
        ordering = ['-id']


class FlowCategory(models.Model):
    uniq_key = models.CharField(max_length=32, unique=True)
    annotation = models.CharField(max_length=16, unique=True)

    # 定义model的元数据
    class Meta:
        # 数据库表名
        verbose_name = 't_flow_category'
        # human readable
        verbose_name_plural = '流程分类定义，便于维护'
        ordering = ['-id']


class BPMN20XML(models.Model):
    uniq_key = models.CharField(max_length=32, unique=True)
    flow_uniq_key = models.CharField(max_length=32)
    bpmn_content = models.TextField()
    version = models.CharField(max_length=16)

    # 定义model的元数据
    class Meta:
        # 数据库表名
        verbose_name = 't_flow_bpmn20xml'
        # human readable
        verbose_name_plural = 'bpmn20xml内容'
        ordering = ['-id']