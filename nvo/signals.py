from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from nvo.models import (OrganizationFinancialYear, People, PaymentRatio, Donations, InfoText,
    Organization, FinancialYear, User, Finance)
from nvo.utils import create_financial_tree

@receiver(post_save, sender=OrganizationFinancialYear)
def create_models_for_organization(sender, instance, created, **kwargs):
    if created:
        create_financial_tree(instance.financial_year_id, instance.organization_id)
        People(year=instance.financial_year, organization=instance.organization).save()
        PaymentRatio(year=instance.financial_year, organization=instance.organization).save()
        Donations(year=instance.financial_year, organization=instance.organization).save()
        Finance(year=instance.financial_year, organization=instance.organization).save()

        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.DONATIONS,
            pre_text=_('donations info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.PROJECTS,
            pre_text=_('projects info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.FINANCE,
            pre_text=_('finance info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.PAYMENTRATIOS,
            pre_text=_('payment ratio info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.PEOPLE,
            pre_text=_('people info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.YEARLYREPORTS,
            pre_text=_('yearly reports info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.BASICINFO,
            pre_text=_('basic info info text')
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
def create_organization_for_user(sender, instance, created, **kwargs):
    if created:
        if not instance.organization:
            organization = Organization(
                name=f'Zacasno ime za {instance.username}',
            )
            organization.save()
            instance.organization = organization
            instance.save()
