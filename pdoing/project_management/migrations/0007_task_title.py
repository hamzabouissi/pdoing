# Generated by Django 3.1.13 on 2021-10-09 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0006_auto_20211009_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(default='', max_length=35),
        ),
    ]
