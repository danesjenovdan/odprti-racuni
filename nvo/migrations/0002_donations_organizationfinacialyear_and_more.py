# Generated by Django 4.0.5 on 2022-07-15 15:08

import django.db.models.deletion
import martor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("nvo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Donations",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("personal_donations_amount", models.IntegerField(default=0)),
                ("number_of_personal_donations", models.IntegerField(default=0)),
                ("organization_donations_amount", models.IntegerField(default=0)),
                ("number_of_organization_donations", models.IntegerField(default=0)),
                (
                    "one_percent_income_tax",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "purpose_of_donations",
                    martor.models.MartorField(verbose_name="Donation purpose"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrganizationFinacialYear",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name="financialyear",
            name="level",
        ),
        migrations.RemoveField(
            model_name="financialyear",
            name="lft",
        ),
        migrations.RemoveField(
            model_name="financialyear",
            name="parent",
        ),
        migrations.RemoveField(
            model_name="financialyear",
            name="rght",
        ),
        migrations.RemoveField(
            model_name="financialyear",
            name="tree_id",
        ),
        migrations.AddField(
            model_name="organization",
            name="financial_years",
            field=models.ManyToManyField(
                related_name="organizations",
                through="nvo.OrganizationFinacialYear",
                to="nvo.financialyear",
            ),
        ),
        migrations.CreateModel(
            name="PersonalDonator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("amount", models.IntegerField(default=0)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="personal_donators",
                        to="nvo.donations",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="organizationfinacialyear",
            name="financial_year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="organiaztion_through",
                to="nvo.financialyear",
            ),
        ),
        migrations.AddField(
            model_name="organizationfinacialyear",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="financial_year_through",
                to="nvo.organization",
            ),
        ),
        migrations.CreateModel(
            name="OrganiaztionDonator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("amount", models.IntegerField(default=0)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organiaztion_donators",
                        to="nvo.donations",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Instructions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "list_instructions",
                    martor.models.MartorField(
                        blank=True,
                        null=True,
                        verbose_name="Instructions for list of objects",
                    ),
                ),
                (
                    "add_instructions",
                    martor.models.MartorField(
                        blank=True,
                        null=True,
                        verbose_name="Instructions for adding object",
                    ),
                ),
                (
                    "edit_instructions",
                    martor.models.MartorField(
                        blank=True,
                        null=True,
                        verbose_name="Instructions for edit single object",
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InfoText",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "card",
                    models.CharField(
                        choices=[
                            ("BI", "BasicInfo"),
                            ("PR", "Projects"),
                            ("DO", "Donations"),
                            ("FI", "Finance"),
                        ],
                        default="BI",
                        max_length=2,
                    ),
                ),
                ("text", models.TextField(default="")),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="info_texts",
                        to="nvo.organization",
                    ),
                ),
                (
                    "year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="info_texts",
                        to="nvo.financialyear",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="donations",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="donations",
                to="nvo.organization",
            ),
        ),
        migrations.AddField(
            model_name="donations",
            name="year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="donations",
                to="nvo.financialyear",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="organizationfinacialyear",
            unique_together={("financial_year", "organization")},
        ),
    ]
