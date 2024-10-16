# Generated by Django 4.0.5 on 2022-07-21 21:04

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nvo", "0004_alter_cofinancer_options_alter_document_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="financialyear",
            options={
                "ordering": ["name"],
                "verbose_name": "Financial year",
                "verbose_name_plural": "Financial years",
            },
        ),
        migrations.AlterModelOptions(
            name="organization",
            options={
                "verbose_name": "Organiaztion",
                "verbose_name_plural": "Organization",
            },
        ),
        migrations.AlterField(
            model_name="employee",
            name="note",
            field=models.TextField(verbose_name="Note"),
        ),
        migrations.AlterField(
            model_name="financialyear",
            name="end_date",
            field=models.DateField(verbose_name="End date"),
        ),
        migrations.AlterField(
            model_name="financialyear",
            name="name",
            field=models.TextField(verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="financialyear",
            name="start_date",
            field=models.DateField(verbose_name="Start date"),
        ),
        migrations.AlterField(
            model_name="organizationfinacialyear",
            name="financial_year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="organiaztion_through",
                to="nvo.financialyear",
                verbose_name="Financial year",
            ),
        ),
        migrations.AlterField(
            model_name="organizationfinacialyear",
            name="is_active",
            field=models.BooleanField(default=False, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="organizationfinacialyear",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="financial_year_through",
                to="nvo.organization",
                verbose_name="Organiaztion",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="organization_share",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MaxValueValidator(100),
                    django.core.validators.MinValueValidator(1),
                ],
                verbose_name="Organization share",
            ),
        ),
    ]
