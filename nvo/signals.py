from django.db.models.signals import post_save
from django.dispatch import receiver

from nvo.models import (OrganizationFinancialYear, People, PaymentRatio, Donations, InfoText,
    Organization, FinancialYear, User)
from nvo.utils import create_financial_tree

@receiver(post_save, sender=OrganizationFinancialYear)
def create_models_for_organization(sender, instance, created, **kwargs):
    if created:
        create_financial_tree(instance.financial_year_id, instance.organization_id)
        People(year=instance.financial_year, organization=instance.organization).save()
        PaymentRatio(year=instance.financial_year, organization=instance.organization).save()
        Donations(year=instance.financial_year, organization=instance.organization).save()

        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.BASICINFO
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.PROJECTS
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.DONATIONS
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.FINANCE
        ).save()

@receiver(post_save, sender=Organization)
def create_organization_financial_year_for_organization(sender, instance, created, **kwargs):
    if created:
        for year in FinancialYear.objects.all():
            OrganizationFinancialYear(
                financial_year=year,
                organization=instance
                ).save()

@receiver(post_save, sender=FinancialYear)
def create_organization_financial_year_for_year(sender, instance, created, **kwargs):
    if created:
        for organization in Organization.objects.all():
            OrganizationFinancialYear(
                financial_year=instance,
                organization=organization
                ).save()

@receiver(post_save, sender=User)
def create_organization_fiinacial_year_for_organization(sender, instance, created, **kwargs):
    if created:
        if not instance.organization:
            organization = Organization(
                name='Zacasno ime',
            )
            organization.save()
            instance.organization = organization
            instance.save()
