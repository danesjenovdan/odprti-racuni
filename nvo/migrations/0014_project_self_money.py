# Generated by Django 4.0.5 on 2022-08-25 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvo', '0013_embed_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='self_money',
            field=models.IntegerField(blank=True, null=True, verbose_name='Self money'),
        ),
    ]