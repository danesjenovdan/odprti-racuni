# Generated by Django 4.0.5 on 2022-08-12 14:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvo', '0006_rename_organizationfinacialyear_organizationfinancialyear_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name': 'Organization', 'verbose_name_plural': 'Organization'},
        ),
        migrations.RemoveField(
            model_name='organization',
            name='city',
        ),
        migrations.AlterField(
            model_name='donations',
            name='number_of_organization_donations',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number od organization donations'),
        ),
        migrations.AlterField(
            model_name='donations',
            name='number_of_personal_donations',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number of personal donations'),
        ),
        migrations.AlterField(
            model_name='donations',
            name='one_percent_income_tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='1 percent income tax'),
        ),
        migrations.AlterField(
            model_name='donations',
            name='organization_donations_amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Organization donations amount'),
        ),
        migrations.AlterField(
            model_name='donations',
            name='personal_donations_amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Personal donation amount'),
        ),
        migrations.AlterField(
            model_name='donations',
            name='purpose_of_donations',
            field=models.TextField(blank=True, null=True, verbose_name='Donation purpose'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='job_share',
            field=models.IntegerField(default=100, validators=[django.core.validators.MinValueValidator(1)], verbose_name='job share'),
        ),
        migrations.AlterField(
            model_name='expensescategory',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.TextField(verbose_name='Organization name'),
        ),
        migrations.AlterField(
            model_name='people',
            name='full_time_employees',
            field=models.IntegerField(null=True, verbose_name='Full time employees'),
        ),
        migrations.AlterField(
            model_name='people',
            name='members',
            field=models.IntegerField(blank=True, null=True, verbose_name='Members'),
        ),
        migrations.AlterField(
            model_name='people',
            name='number_of_men',
            field=models.IntegerField(null=True, verbose_name='Number of men'),
        ),
        migrations.AlterField(
            model_name='people',
            name='number_of_non_binary',
            field=models.IntegerField(null=True, verbose_name='Number of non binary'),
        ),
        migrations.AlterField(
            model_name='people',
            name='number_of_women',
            field=models.IntegerField(null=True, verbose_name='Number of women'),
        ),
        migrations.AlterField(
            model_name='people',
            name='other_employees',
            field=models.IntegerField(null=True, verbose_name='Other employees'),
        ),
        migrations.AlterField(
            model_name='people',
            name='volunteers',
            field=models.IntegerField(blank=True, null=True, verbose_name='Volunteers'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.TextField(verbose_name='Project name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='organization_share',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Organization share'),
        ),
        migrations.AlterField(
            model_name='revenuecategory',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Amount'),
        ),
    ]