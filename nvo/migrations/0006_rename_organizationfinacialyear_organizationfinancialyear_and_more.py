# Generated by Django 4.0.5 on 2022-08-01 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("nvo", "0005_alter_financialyear_options_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="OrganizationFinacialYear",
            new_name="OrganizationFinancialYear",
        ),
        migrations.AlterModelOptions(
            name="people",
            options={"verbose_name": "People", "verbose_name_plural": "People"},
        ),
    ]
