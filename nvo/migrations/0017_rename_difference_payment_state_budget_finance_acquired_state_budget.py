# Generated by Django 4.0.5 on 2022-10-07 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("nvo", "0016_alter_finance_amount_voluntary_work_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="finance",
            old_name="difference_payment_state_budget",
            new_name="acquired_state_budget",
        ),
    ]
