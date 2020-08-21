# Generated by Django 2.2 on 2020-08-21 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow_manage', '0007_auto_20200819_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlowInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flowable_id', models.CharField(max_length=32, unique=True)),
                ('start_user_id', models.CharField(max_length=16)),
                ('start_time', models.DateTimeField(help_text='创建时间')),
                ('bpmn_uid', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'flow_instance',
                'verbose_name_plural': 'flow_instances',
                'db_table': 'flow_instance',
                'ordering': ['-id'],
            },
        ),
        migrations.RenameField(
            model_name='bpmn',
            old_name='bpmn_content',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='bpmn',
            old_name='flow_uniq_key',
            new_name='flow_uid',
        ),
        migrations.RenameField(
            model_name='bpmn',
            old_name='uniq_key',
            new_name='uid',
        ),
        migrations.RenameField(
            model_name='flowcategory',
            old_name='uniq_key',
            new_name='uid',
        ),
        migrations.RenameField(
            model_name='flowdefinition',
            old_name='online_bpmn_key',
            new_name='bpmn_uid',
        ),
        migrations.RenameField(
            model_name='flowdefinition',
            old_name='uniq_key',
            new_name='uid',
        ),
        migrations.RenameField(
            model_name='flowdefinition',
            old_name='uniq_name',
            new_name='uname',
        ),
    ]
