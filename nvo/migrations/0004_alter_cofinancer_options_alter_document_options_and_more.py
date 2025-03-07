# Generated by Django 4.0.5 on 2022-07-20 09:00

import django.core.validators
import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("nvo", "0003_rename_end_time_financialyear_end_date_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cofinancer",
            options={
                "verbose_name": "Cofinancer",
                "verbose_name_plural": "Cofinancers",
            },
        ),
        migrations.AlterModelOptions(
            name="document",
            options={"verbose_name": "Document", "verbose_name_plural": "Documents"},
        ),
        migrations.AlterModelOptions(
            name="documentcategory",
            options={
                "verbose_name": "Document category",
                "verbose_name_plural": "Document categories",
            },
        ),
        migrations.AlterModelOptions(
            name="donations",
            options={"verbose_name": "Donations", "verbose_name_plural": "Donations"},
        ),
        migrations.AlterModelOptions(
            name="donator",
            options={"verbose_name": "Donator", "verbose_name_plural": "Donators"},
        ),
        migrations.AlterModelOptions(
            name="employee",
            options={"verbose_name": "Employee", "verbose_name_plural": "Employees"},
        ),
        migrations.AlterModelOptions(
            name="expensescategory",
            options={"verbose_name": "Expense", "verbose_name_plural": "Expenses"},
        ),
        migrations.AlterModelOptions(
            name="financer",
            options={"verbose_name": "Financer", "verbose_name_plural": "Financers"},
        ),
        migrations.AlterModelOptions(
            name="financialyear",
            options={
                "verbose_name": "Financial year",
                "verbose_name_plural": "Financial years",
            },
        ),
        migrations.AlterModelOptions(
            name="infotext",
            options={"verbose_name": "Info Text", "verbose_name_plural": "Info Texts"},
        ),
        migrations.AlterModelOptions(
            name="instructions",
            options={
                "verbose_name": "Instructions",
                "verbose_name_plural": "Instructions",
            },
        ),
        migrations.AlterModelOptions(
            name="organiaztiondonator",
            options={
                "verbose_name": "OrganiaztionDonator",
                "verbose_name_plural": "OrganiaztionDonators",
            },
        ),
        migrations.AlterModelOptions(
            name="organization",
            options={
                "verbose_name": "Organiaztion",
                "verbose_name_plural": "Ogranizations",
            },
        ),
        migrations.AlterModelOptions(
            name="organizationfinacialyear",
            options={
                "verbose_name": "Organiaztion financial year",
                "verbose_name_plural": "Organiaztion financial years",
            },
        ),
        migrations.AlterModelOptions(
            name="partner",
            options={"verbose_name": "Partner", "verbose_name_plural": "Partners"},
        ),
        migrations.AlterModelOptions(
            name="paymentratio",
            options={
                "verbose_name": "Payment ratio",
                "verbose_name_plural": "Payment ratios",
            },
        ),
        migrations.AlterModelOptions(
            name="people",
            options={"verbose_name": "Perople", "verbose_name_plural": "People"},
        ),
        migrations.AlterModelOptions(
            name="personaldonator",
            options={
                "verbose_name": "PersonalDonator",
                "verbose_name_plural": "PersonalDonators",
            },
        ),
        migrations.AlterModelOptions(
            name="project",
            options={"verbose_name": "Project", "verbose_name_plural": "Projects"},
        ),
        migrations.AlterModelOptions(
            name="revenuecategory",
            options={"verbose_name": "Revenue", "verbose_name_plural": "Revenues"},
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "User", "verbose_name_plural": "Users"},
        ),
        migrations.RemoveField(
            model_name="people",
            name="employees_by_hours",
        ),
        migrations.AlterField(
            model_name="cofinancer",
            name="logo",
            field=models.FileField(
                blank=True, null=True, upload_to="", verbose_name="Logo"
            ),
        ),
        migrations.AlterField(
            model_name="cofinancer",
            name="name",
            field=models.TextField(verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="document",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="nvo.documentcategory",
                verbose_name="Category",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="file",
            field=models.FileField(upload_to="", verbose_name="File"),
        ),
        migrations.AlterField(
            model_name="document",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="documents",
                to="nvo.organization",
                verbose_name="Organiaztion",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="documents",
                to="nvo.financialyear",
                verbose_name="Year",
            ),
        ),
        migrations.AlterField(
            model_name="documentcategory",
            name="name",
            field=models.TextField(verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="donations",
            name="number_of_organization_donations",
            field=models.IntegerField(
                default=0, verbose_name="Number od organization donations"
            ),
        ),
        migrations.AlterField(
            model_name="donations",
            name="number_of_personal_donations",
            field=models.IntegerField(
                default=0, verbose_name="Number of personal donations"
            ),
        ),
        migrations.AlterField(
            model_name="donations",
            name="one_percent_income_tax",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="1 percent income tax",
            ),
        ),
        migrations.AlterField(
            model_name="donations",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="donations",
                to="nvo.organization",
                verbose_name="Organization",
            ),
        ),
        migrations.AlterField(
            model_name="donations",
            name="organization_donations_amount",
            field=models.IntegerField(
                default=0, verbose_name="Organization donations amount"
            ),
        ),
        migrations.AlterField(
            model_name="donations",
            name="personal_donations_amount",
            field=models.IntegerField(
                default=0, verbose_name="Personal donation amount"
            ),
        ),
        migrations.AlterField(
            model_name="donations",
            name="year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="donations",
                to="nvo.financialyear",
                verbose_name="Year",
            ),
        ),
        migrations.AlterField(
            model_name="donator",
            name="name",
            field=models.TextField(verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="employee",
            name="average_gross_salary",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="Average gross selary"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="job_share",
            field=models.IntegerField(
                default=100,
                validators=[
                    django.core.validators.MaxValueValidator(100),
                    django.core.validators.MinValueValidator(1),
                ],
                verbose_name="job share",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="note",
            field=models.TextField(verbose_name="Node"),
        ),
        migrations.AlterField(
            model_name="expensescategory",
            name="additional_name",
            field=models.CharField(
                blank=True, max_length=256, null=True, verbose_name="Additional name"
            ),
        ),
        migrations.AlterField(
            model_name="expensescategory",
            name="allow_additional_name",
            field=models.BooleanField(
                default=False, verbose_name="Allow additional name"
            ),
        ),
        migrations.AlterField(
            model_name="expensescategory",
            name="amount",
            field=models.DecimalField(
                decimal_places=2, default=0.0, max_digits=10, verbose_name="Amount"
            ),
        ),
        migrations.AlterField(
            model_name="expensescategory",
            name="instructions",
            field=models.TextField(verbose_name="Instructions"),
        ),
        migrations.AlterField(
            model_name="expensescategory",
            name="name",
            field=models.CharField(max_length=256, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="expensescategory",
            name="order",
            field=models.IntegerField(verbose_name="Order"),
        ),
        migrations.AlterField(
            model_name="expensescategory",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_related",
                to="nvo.organization",
                verbose_name="Organiaztion",
            ),
        ),
        migrations.AlterField(
            model_name="expensescategory",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="categories_children",
                to="nvo.expensescategory",
                verbose_name="Parent",
            ),
        ),
        migrations.AlterField(
            model_name="expensescategory",
            name="year",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_related",
                to="nvo.financialyear",
                verbose_name="Year",
            ),
        ),
        migrations.AlterField(
            model_name="financer",
            name="logo",
            field=models.FileField(
                blank=True, null=True, upload_to="", verbose_name="Logo"
            ),
        ),
        migrations.AlterField(
            model_name="financer",
            name="name",
            field=models.TextField(verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="infotext",
            name="card",
            field=models.CharField(
                choices=[
                    ("BI", "BasicInfo"),
                    ("PR", "Projects"),
                    ("DO", "Donations"),
                    ("FI", "Finance"),
                ],
                default="BI",
                max_length=2,
                verbose_name="Card",
            ),
        ),
        migrations.AlterField(
            model_name="infotext",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="info_texts",
                to="nvo.organization",
                verbose_name="Organization",
            ),
        ),
        migrations.AlterField(
            model_name="infotext",
            name="text",
            field=models.TextField(default="", verbose_name="Text"),
        ),
        migrations.AlterField(
            model_name="infotext",
            name="year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="info_texts",
                to="nvo.financialyear",
                verbose_name="Year",
            ),
        ),
        migrations.AlterField(
            model_name="instructions",
            name="model",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
                verbose_name="Model",
            ),
        ),
        migrations.AlterField(
            model_name="organiaztiondonator",
            name="amount",
            field=models.IntegerField(default=0, verbose_name="Amount"),
        ),
        migrations.AlterField(
            model_name="organiaztiondonator",
            name="name",
            field=models.TextField(verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="address",
            field=models.TextField(null=True, verbose_name="Address"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="city",
            field=models.TextField(null=True, verbose_name="Post"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="email",
            field=models.EmailField(max_length=254, null=True, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="financial_years",
            field=models.ManyToManyField(
                related_name="organizations",
                through="nvo.OrganizationFinacialYear",
                to="nvo.financialyear",
                verbose_name="Financial years",
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="is_charity",
            field=models.BooleanField(default=False, verbose_name="is charity"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="is_for_the_public_good",
            field=models.TextField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Is organization for public good",
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="logo",
            field=models.ImageField(null=True, upload_to="", verbose_name="Logo"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="name",
            field=models.TextField(verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="phone_number",
            field=models.CharField(
                blank=True, max_length=13, null=True, verbose_name="Phone number"
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="post_number",
            field=models.TextField(null=True, verbose_name="Post number"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="registration_number",
            field=models.TextField(null=True, verbose_name="Registration number"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="representative",
            field=models.TextField(null=True, verbose_name="representative"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="tax_number",
            field=models.CharField(max_length=10, null=True, verbose_name="TAX number"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="trr",
            field=models.TextField(null=True, verbose_name="TRR"),
        ),
        migrations.AlterField(
            model_name="partner",
            name="name",
            field=models.TextField(verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="paymentratio",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment_ratios",
                to="nvo.organization",
                verbose_name="Organiaztion",
            ),
        ),
        migrations.AlterField(
            model_name="paymentratio",
            name="year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment_ratios",
                to="nvo.financialyear",
                verbose_name="Year",
            ),
        ),
        migrations.AlterField(
            model_name="people",
            name="full_time_employees",
            field=models.IntegerField(default=0, verbose_name="Full time employees"),
        ),
        migrations.AlterField(
            model_name="people",
            name="members",
            field=models.IntegerField(default=0, verbose_name="Members"),
        ),
        migrations.AlterField(
            model_name="people",
            name="number_of_men",
            field=models.IntegerField(default=0, verbose_name="Number of men"),
        ),
        migrations.AlterField(
            model_name="people",
            name="number_of_non_binary",
            field=models.IntegerField(default=0, verbose_name="Number of non binary"),
        ),
        migrations.AlterField(
            model_name="people",
            name="number_of_women",
            field=models.IntegerField(default=0, verbose_name="Number of women"),
        ),
        migrations.AlterField(
            model_name="people",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="people",
                to="nvo.organization",
                verbose_name="Organiaztion",
            ),
        ),
        migrations.AlterField(
            model_name="people",
            name="other_employees",
            field=models.IntegerField(default=0, verbose_name="Other employees"),
        ),
        migrations.AlterField(
            model_name="people",
            name="volunteers",
            field=models.IntegerField(default=0, verbose_name="Volunteers"),
        ),
        migrations.AlterField(
            model_name="people",
            name="year",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="people",
                to="nvo.financialyear",
                verbose_name="Year",
            ),
        ),
        migrations.AlterField(
            model_name="personaldonator",
            name="amount",
            field=models.IntegerField(default=0, verbose_name="Amount"),
        ),
        migrations.AlterField(
            model_name="personaldonator",
            name="name",
            field=models.TextField(verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="project",
            name="end_date",
            field=models.DateField(verbose_name="End date"),
        ),
        migrations.AlterField(
            model_name="project",
            name="name",
            field=models.TextField(verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="project",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="projects",
                to="nvo.organization",
                verbose_name="Organization",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="organization_share",
            field=models.IntegerField(verbose_name="Organization share"),
        ),
        migrations.AlterField(
            model_name="project",
            name="start_date",
            field=models.DateField(verbose_name="Start date"),
        ),
        migrations.AlterField(
            model_name="project",
            name="value",
            field=models.IntegerField(verbose_name="Total value"),
        ),
        migrations.AlterField(
            model_name="revenuecategory",
            name="additional_name",
            field=models.CharField(
                blank=True, max_length=256, null=True, verbose_name="Additional name"
            ),
        ),
        migrations.AlterField(
            model_name="revenuecategory",
            name="allow_additional_name",
            field=models.BooleanField(
                default=False, verbose_name="Allow additional name"
            ),
        ),
        migrations.AlterField(
            model_name="revenuecategory",
            name="amount",
            field=models.DecimalField(
                decimal_places=2, default=0.0, max_digits=10, verbose_name="Amount"
            ),
        ),
        migrations.AlterField(
            model_name="revenuecategory",
            name="instructions",
            field=models.TextField(verbose_name="Instructions"),
        ),
        migrations.AlterField(
            model_name="revenuecategory",
            name="name",
            field=models.CharField(max_length=256, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="revenuecategory",
            name="order",
            field=models.IntegerField(verbose_name="Order"),
        ),
        migrations.AlterField(
            model_name="revenuecategory",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_related",
                to="nvo.organization",
                verbose_name="Organiaztion",
            ),
        ),
        migrations.AlterField(
            model_name="revenuecategory",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="categories_children",
                to="nvo.revenuecategory",
                verbose_name="Parent",
            ),
        ),
        migrations.AlterField(
            model_name="revenuecategory",
            name="year",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_related",
                to="nvo.financialyear",
                verbose_name="Year",
            ),
        ),
    ]
