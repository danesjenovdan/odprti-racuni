# Generated by Django 4.0.5 on 2023-02-28 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nvo", "0024_embed_page_of_embed_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentratio",
            name="highest_absolute_salary",
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name="paymentratio",
            name="highest_salary",
            field=models.FloatField(default=1),
        ),
    ]
