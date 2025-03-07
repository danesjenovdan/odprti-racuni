# Generated by Django 4.0.5 on 2022-08-22 18:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nvo", "0012_embed_alter_finance_options_alter_document_file_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="embed",
            name="organization",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="embeds",
                to="nvo.organization",
                verbose_name="Organization",
            ),
            preserve_default=False,
        ),
    ]
