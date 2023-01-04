from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from nvo.models import (OrganizationFinancialYear, People, PaymentRatio, Donations, InfoText,
    Organization, FinancialYear, User, Finance, Embed)
from nvo.utils import create_financial_tree

@receiver(post_save, sender=OrganizationFinancialYear)
def create_models_for_organization(sender, instance, created, **kwargs):
    if created:
        create_financial_tree(instance.financial_year_id, instance.organization_id)
        People(year=instance.financial_year, organization=instance.organization).save()
        PaymentRatio(year=instance.financial_year, organization=instance.organization).save()
        Donations(year=instance.financial_year, organization=instance.organization).save()
        Finance(year=instance.financial_year, organization=instance.organization).save()

        # donations
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.DONATION_CONSUMPTION,
            pre_text=_('donations purpose info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.INCOME_TAX,
            pre_text=_('one percent tax info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.ORG_DONATIONS,
            pre_text=_('Organizatin donations text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.PERSONAL_DONATIONS,
            pre_text=_('Personal donation text')
        ).save()

        # projects
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.PROJECTS,
            pre_text=_('projects info text')
        ).save()

        # finance
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.STATE_BUDGET,
            pre_text=_('Payment to the state budget info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.PRO_PARTNERS,
            pre_text=_('Payments to projects partners info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.VOLUNTIER,
            pre_text=_('Amount of voluntary work info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.EXPENSE,
            pre_text=_('Expense info text')
        ).save()
        InfoText(
            year=instance.financial_year,
            organization=instance.organization,
            card=InfoText.CardTypes.REVENUE,
            pre_text=_('Revenue info text')
        ).save()

        # basic info
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
        embed = Embed(organization=instance)
        embed.save()
        for year in FinancialYear.objects.all():
            OrganizationFinancialYear(
                financial_year=year,
                organization=instance,
                embed=embed
                ).save()

@receiver(post_save, sender=FinancialYear)
def create_organization_financial_year_for_year(sender, instance, created, **kwargs):
    if created:
        for organization in Organization.objects.all():
            OrganizationFinancialYear(
                financial_year=instance,
                organization=organization,
                embed=organization.embeds.first()
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
