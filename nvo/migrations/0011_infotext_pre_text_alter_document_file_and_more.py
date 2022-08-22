# Generated by Django 4.0.5 on 2022-08-17 08:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvo', '0010_finance_difference_payment_state_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='infotext',
            name='pre_text',
            field=models.TextField(default='', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'xls'])], verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='infotext',
            name='card',
            field=models.CharField(choices=[('BI', 'BasicInfo'), ('YR', 'Documents'), ('PE', 'People'), ('PS', 'Payment ratios'), ('PR', 'Projects'), ('DO', 'Donations'), ('FI', 'Finance')], default='BI', max_length=2, verbose_name='Card'),
        ),
    ]