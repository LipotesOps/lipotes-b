# Generated by Django 2.2 on 2020-08-21 03:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200821_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_secret',
            field=models.UUIDField(default=uuid.UUID('eb97021b-8abf-4559-a6fc-a132f74b569d')),
        ),
    ]
