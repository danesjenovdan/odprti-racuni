from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from datetime import datetime, date

from nvo import models



class Command(BaseCommand):
    help = 'Setup data'
    def handle(self, *args, **options):
        self.view_options = [('view_', 'Can view ')]
        self.edit_options = [('change_', 'Can change '), ('view_', 'Can view ')]
        self.edit_create_options = [('add_', 'Can add '),('change_', 'Can change '), ('view_', 'Can view ')]
        self.edit_create_delete_options = [('add_', 'Can add '), ('change_', 'Can change '), ('view_', 'Can view '), ('delete_', 'Can delete ')]

        models.FinancialYear.objects.get_or_create(
            name='2021',
            start_date=date(day=1, month=1, year=2021),
            end_date=date(day=31, month=12, year=2021)
        )

        models.DocumentCategory.objects.get_or_create(
            name='vsebinsko poročilo'
        )
        models.DocumentCategory.objects.get_or_create(
            name='finančno poročilo'
        )
        models.DocumentCategory.objects.get_or_create(
            name='skupno vsebinsko in finančno poročilo'
        )
        models.DocumentCategory.objects.get_or_create(
            name='poročilo o prostovoljskem delu'
        )

        nvo_group, created = Group.objects.get_or_create(
            name='Nvo user',
        )

        ct = ContentType.objects.get_for_model(models.Organization)
        permissions = self.get_permissions('organization', ct, self.edit_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.FinancialYear)
        permissions = self.get_permissions('financialyear', ct, self.view_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.OrganizationFinacialYear)
        permissions = self.get_permissions('organizationfinacialyear', ct, self.edit_create_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.DocumentCategory)
        permissions = self.get_permissions('documentcategory', ct, self.view_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.Document)
        permissions = self.get_permissions('document', ct, self.edit_create_delete_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.People)
        permissions = self.get_permissions('people', ct, self.edit_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.PaymentRatio)
        permissions = self.get_permissions('paymentratio', ct, self.edit_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.Employee)
        permissions = self.get_permissions('employee', ct, self.edit_create_delete_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.RevenueCategory)
        permissions = self.get_permissions('revenuecategory', ct, self.edit_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.ExpensesCategory)
        permissions = self.get_permissions('expensescategory', ct, self.edit_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.Project)
        permissions = self.get_permissions('project', ct, self.edit_create_delete_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.Financer)
        permissions = self.get_permissions('financer', ct, self.edit_create_delete_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.CoFinancer)
        permissions = self.get_permissions('cofinancer', ct, self.edit_create_delete_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.Partner)
        permissions = self.get_permissions('partner', ct, self.edit_create_delete_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.Donator)
        permissions = self.get_permissions('donator', ct, self.edit_create_delete_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.Donations)
        permissions = self.get_permissions('donations', ct, self.edit_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.PersonalDonator)
        permissions = self.get_permissions('personaldonator', ct, self.edit_create_delete_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.OrganiaztionDonator)
        permissions = self.get_permissions('organiaztiondonator', ct, self.edit_create_delete_options)
        nvo_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.InfoText)
        permissions = self.get_permissions('infotext', ct, self.edit_options)
        nvo_group.permissions.add(*permissions)

    def get_permissions(self, name, ct, options=[('view_', 'Can view ')]):
        permissions = []
        for option in options:
            print(f'{option[0]}{name}')
            permissions.append(Permission.objects.get(
            codename=f'{option[0]}{name}'))
        return permissions
