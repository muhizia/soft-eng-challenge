# Generated by Django 3.2.12 on 2022-05-10 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('military_base', '0002_auto_20220509_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crewmember',
            name='code',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='crewmember',
            name='firstName',
            field=models.CharField(max_length=200),
        ),
    ]