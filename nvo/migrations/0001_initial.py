# Generated by Django 4.0.5 on 2022-07-13 07:22

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import martor.models
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('start_time', models.DateField()),
                ('end_time', models.DateField()),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='none', to='nvo.financialyear')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('logo', models.ImageField(null=True, upload_to='')),
                ('address', models.TextField(null=True)),
                ('city', models.TextField(null=True)),
                ('post_number', models.TextField(null=True)),
                ('tax_number', models.CharField(max_length=10, null=True)),
                ('registration_number', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True)),
                ('trr', models.TextField(null=True)),
                ('representative', models.TextField(null=True)),
                ('is_charity', models.BooleanField(default=False)),
                ('is_for_the_public_good', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RevenueCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('additional_name', models.CharField(blank=True, max_length=256, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order', models.IntegerField()),
                ('instructions', models.TextField()),
                ('allow_additional_name', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='nvo.organization')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories_children', to='nvo.revenuecategory')),
                ('year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='nvo.financialyear')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', martor.models.MartorField(verbose_name="Project's description")),
                ('outcomes_and_impacts', martor.models.MartorField(verbose_name="Project's outcomes and impacts")),
                ('link', models.URLField(blank=True, null=True, verbose_name="Project's link")),
                ('value', models.IntegerField()),
                ('organization_share', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='nvo.organization')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='nvo.financialyear')),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_time_employees', models.IntegerField(default=0)),
                ('other_employees', models.IntegerField(default=0)),
                ('volunteers', models.IntegerField(default=0)),
                ('members', models.IntegerField(default=0)),
                ('number_of_men', models.IntegerField(default=0)),
                ('number_of_women', models.IntegerField(default=0)),
                ('number_of_non_binary', models.IntegerField(default=0)),
                ('employees_by_hours', models.IntegerField(default=0)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='people', to='nvo.organization')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='people', to='nvo.financialyear')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRatio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_ratios', to='nvo.organization')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_ratios', to='nvo.financialyear')),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('link', models.URLField(blank=True, null=True, verbose_name="Partners's link")),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='nvo.project')),
            ],
        ),
        migrations.CreateModel(
            name='Financer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('link', models.URLField(blank=True, null=True, verbose_name="Financer's link")),
                ('logo', models.FileField(blank=True, null=True, upload_to='')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financers', to='nvo.project')),
            ],
        ),
        migrations.CreateModel(
            name='ExpensesCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('additional_name', models.CharField(blank=True, max_length=256, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order', models.IntegerField()),
                ('instructions', models.TextField()),
                ('allow_additional_name', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='nvo.organization')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories_children', to='nvo.expensescategory')),
                ('year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='nvo.financialyear')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('average_gross_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('job_share', models.IntegerField(default=100, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('payment_ratio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='nvo.paymentratio')),
            ],
        ),
        migrations.CreateModel(
            name='Donator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('link', models.URLField(blank=True, null=True, verbose_name="Donators's link")),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donators', to='nvo.project')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nvo.documentcategory')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='nvo.organization')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='nvo.financialyear')),
            ],
        ),
        migrations.CreateModel(
            name='CoFinancer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('link', models.URLField(blank=True, null=True, verbose_name="CoFinancer's link")),
                ('logo', models.FileField(blank=True, null=True, upload_to='')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cofinancers', to='nvo.project')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='nvo.organization', verbose_name='Organization')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
