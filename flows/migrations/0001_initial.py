# Generated by Django 2.2 on 2020-09-04 09:22

from django.db import migrations, models
import django.db.models.deletion
import flows.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlowBpmn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctime', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
                ('mtime', models.DateTimeField(auto_now=True, help_text='修改时间')),
                ('uuid', models.CharField(default=uuid.uuid1, editable=False, max_length=64, unique=True, verbose_name='UUID')),
                ('tag', models.CharField(default=flows.models.genTagNum, editable=False, max_length=32)),
                ('content', models.TextField()),
                ('flowable_process_definition_id', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('status', models.CharField(choices=[('draft', '草稿'), ('online', '生效'), ('offline', '下线'), ('del', '删除')], default='draft', max_length=32)),
            ],
            options={
                'verbose_name': 'flow_bpmn',
                'verbose_name_plural': 'flow_bpmns',
                'db_table': 'flow_bpmn',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='FlowCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctime', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
                ('mtime', models.DateTimeField(auto_now=True, help_text='修改时间')),
                ('uuid', models.CharField(default=uuid.uuid1, editable=False, max_length=64, unique=True, verbose_name='UUID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name': 'flow_category',
                'verbose_name_plural': 'flow_categories',
                'db_table': 'flow_category',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='FlowInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid1, editable=False, max_length=64, unique=True, verbose_name='UUID')),
                ('ctime', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
                ('mtime', models.DateTimeField(auto_now=True, help_text='修改时间')),
                ('flowable_process_instance_id', models.CharField(max_length=64, unique=True)),
                ('start_user_id', models.CharField(max_length=32)),
                ('start_time', models.DateTimeField(help_text='创建时间')),
            ],
            options={
                'verbose_name': 'flow_instance',
                'verbose_name_plural': 'flow_instances',
                'db_table': 'flow_instance',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TaskInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flowable_task_instance_id', models.CharField(max_length=64, unique=True)),
                ('task_definition_key', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('create_time', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'task_instance',
                'verbose_name_plural': 'task_instances',
                'db_table': 'task_instance',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid1, editable=False, max_length=64, unique=True, verbose_name='UUID')),
                ('ctime', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
                ('mtime', models.DateTimeField(auto_now=True, help_text='修改时间')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('extend_fields', models.TextField(default={})),
                ('bpmn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_bpmn', to='flows.FlowBpmn', to_field='uuid')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_category', to='flows.FlowCategory', to_field='uuid')),
            ],
            options={
                'verbose_name': 'flows',
                'verbose_name_plural': '流程定义',
                'db_table': 'flow',
                'ordering': ['-id'],
            },
        ),
    ]
