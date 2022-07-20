from django.db.models.signals import post_save
from django.dispatch import receiver

from nvo.models import OrganizationFinacialYear, People, PaymentRatio, Donations, InfoText
from nvo.utils import create_financial_tree

@receiver(post_save, sender=OrganizationFinacialYear)
def create_models_for_organization(sender, instance, created, **kwargs):
    if created:
        create_financial_tree(instance.financial_year_id, instance.organization_id)
        People(year=instance.financial_year, organization=instance.organization).save()
        PaymentRatio(year=instance.financial_year, organization=instance.organization).save()
        Donations(year=instance.financial_year, organization=instance.organization).save()

        InfoText(year=instance.financial_year, organization=instance.organization, card=InfoText.CardTypes.BASICINFO).save()
        InfoText(year=instance.financial_year, organization=instance.organization, card=InfoText.CardTypes.PROJECTS).save()
        InfoText(year=instance.financial_year, organization=instance.organization, card=InfoText.CardTypes.DONATIONS).save()
        InfoText(year=instance.financial_year, organization=instance.organization, card=InfoText.CardTypes.FINANCE).save()
