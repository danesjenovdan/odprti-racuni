# Generated by Django 4.0.5 on 2023-03-23 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nvo', '0026_alter_paymentratio_highest_absolute_salary_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donations',
            options={'ordering': ['-year__name'], 'verbose_name': 'Donations', 'verbose_name_plural': 'Donations'},
        ),
        migrations.AlterModelOptions(
            name='finance',
            options={'ordering': ['-year__name'], 'verbose_name': 'Finance', 'verbose_name_plural': 'Finance'},
        ),
        migrations.AlterModelOptions(
            name='financialyear',
            options={'ordering': ['-name'], 'verbose_name': 'Financial year', 'verbose_name_plural': 'Financial years'},
        ),
        migrations.AlterModelOptions(
            name='infotext',
            options={'ordering': ['-year__name'], 'verbose_name': 'Info Text', 'verbose_name_plural': 'Info Texts'},
        ),
        migrations.AlterModelOptions(
            name='paymentratio',
            options={'ordering': ['-year__name'], 'verbose_name': 'Payment ratio', 'verbose_name_plural': 'Payment ratios'},
        ),
        migrations.AlterModelOptions(
            name='people',
            options={'ordering': ['-year__name'], 'verbose_name': 'People', 'verbose_name_plural': 'People'},
        ),
        migrations.AddField(
            model_name='expensescategory',
            name='aop',
            field=models.CharField(blank=True, max_length=256, verbose_name='AOP'),
        ),
        migrations.AddField(
            model_name='revenuecategory',
            name='aop',
            field=models.CharField(blank=True, max_length=256, verbose_name='AOP'),
        ),
    ]
