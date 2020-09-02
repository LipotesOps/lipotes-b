# Generated by Django 2.2 on 2020-09-02 14:16

from django.db import migrations, models
import flow_manage.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BPMN',
            fields=[
                ('id', models.CharField(default=uuid.uuid1, editable=False, max_length=64, primary_key=True, serialize=False, unique=True, verbose_name='流程定义bpmn版本ID')),
                ('version', models.CharField(default=flow_manage.models.generateVersionNum, editable=False, max_length=32)),
                ('content', models.TextField()),
                ('flowable_process_definition_id', models.CharField(max_length=64, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'flow_definition_version',
                'verbose_name_plural': 'flow_definition_versions',
                'db_table': 'flow_definition_version',
                'ordering': ['-version'],
            },
        ),
        migrations.CreateModel(
            name='FlowCategory',
            fields=[
                ('id', models.CharField(default=uuid.uuid1, editable=False, max_length=64, primary_key=True, serialize=False, unique=True, verbose_name='流程分类ID')),
                ('uname', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name': 'flow_definition_category',
                'verbose_name_plural': 'flow_definition_categories',
                'db_table': 'flow_definition_category',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='FlowDefinition',
            fields=[
                ('id', models.CharField(default=uuid.uuid1, editable=False, max_length=64, primary_key=True, serialize=False, unique=True, verbose_name='流程定义ID')),
                ('uname', models.CharField(max_length=32, unique=True)),
                ('category', models.CharField(max_length=32)),
                ('version_id', models.CharField(max_length=64, verbose_name='流程定义版本ID')),
                ('status', models.CharField(choices=[('draft', '草稿'), ('online', '生效'), ('offline', '下线'), ('del', '删除')], default='draft', max_length=32)),
                ('extend_fields', models.TextField(default={})),
                ('ctime', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
                ('mtime', models.DateTimeField(auto_now_add=True, help_text='修改时间')),
            ],
            options={
                'verbose_name': 'flow_definitions',
                'verbose_name_plural': '流程定义',
                'db_table': 'flow_definition',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='FlowInstance',
            fields=[
                ('id', models.CharField(default=uuid.uuid1, editable=False, max_length=64, primary_key=True, serialize=False, unique=True, verbose_name='流程实例ID')),
                ('flowable_process_instance_id', models.CharField(max_length=64, unique=True)),
                ('start_user_id', models.CharField(max_length=32)),
                ('start_time', models.DateTimeField(help_text='创建时间')),
                ('definition_id', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'flow_instance',
                'verbose_name_plural': 'flow_instances',
                'db_table': 'flow_inst',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TaskInstance',
            fields=[
                ('id', models.CharField(default=uuid.uuid1, editable=False, max_length=64, primary_key=True, serialize=False, unique=True, verbose_name='任务实例ID')),
                ('flowable_task_instance_id', models.CharField(max_length=64, unique=True)),
                ('taskDefinitionKey', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('create_time', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'task_instance',
                'verbose_name_plural': 'task_instances',
                'db_table': 'task_inst',
                'ordering': ['-id'],
            },
        ),
    ]
