# Generated by Django 4.0.5 on 2022-08-25 14:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvo', '0014_project_self_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='job_share',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='job share'),
        ),
    ]
