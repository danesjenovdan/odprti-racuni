# Generated by Django 4.1.5 on 2023-01-13 12:54

from django.db import migrations, models

import nvo.models


class Migration(migrations.Migration):

    dependencies = [
        ("nvo", "0022_organizationfinancialyear_embed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cofinancer",
            name="logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="",
                validators=[
                    nvo.models.image_validator,
                    nvo.models.validate_image_extension,
                ],
                verbose_name="Logo",
            ),
        ),
        migrations.AlterField(
            model_name="financer",
            name="logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="",
                validators=[
                    nvo.models.image_validator,
                    nvo.models.validate_image_extension,
                ],
                verbose_name="Logo",
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="logo",
            field=models.ImageField(
                null=True,
                upload_to="",
                validators=[
                    nvo.models.image_validator,
                    nvo.models.validate_image_extension,
                ],
                verbose_name="Logo",
            ),
        ),
    ]
