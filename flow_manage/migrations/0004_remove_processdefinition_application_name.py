# Generated by Django 2.2 on 2020-06-22 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flow_manage', '0003_auto_20200615_0752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processdefinition',
            name='application_name',
        ),
    ]
