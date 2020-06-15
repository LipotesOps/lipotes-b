
from datetime import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class ProcessDefinition(models.Model):
    status_choices = {
        'draf': '草稿',
        'on': '生效',
        'off': '下线',
        'del': '删除'
    }

    application_name = models.CharField(max_length=50, default='')
    pkey = models.CharField(max_length=255)
    pname = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    bpmn2 = models.TextField()
    status = models.CharField(max_length=255, default='draft', choices=status_choices.items())

    ctime = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    mtime = models.DateTimeField(auto_now_add=True, help_text=u'修改时间')

    #   定义model的元数据
    class Meta:
        # 数据库表名
        verbose_name = 'ProcessDefinition'
        # human readable
        verbose_name_plural = '流程定义'
        ordering = ['-id']