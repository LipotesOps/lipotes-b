from django.db import models

# Create your models here.

class ProcessDefinition(models.Model):

    application_name = models.CharField(max_length=50, default='')
    pkey = models.CharField(max_length=255)
    pname = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    bpmn2 = models.TextField()

    #   定义model的元数据
    class Meta:
        # 数据库表名
        verbose_name = 'ProcessDefinition'
        # human readable
        verbose_name_plural = '流程定义'
        ordering = ['-id']