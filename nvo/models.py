from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from mptt.models import MPTTModel, TreeForeignKey
from martor.models import MartorField
from dateutil import relativedelta

from nvo.behaviors.models import Timestampable

# Create your models here.

class User(AbstractUser, Timestampable):
    organization = models.ForeignKey(
        'Organization',
        blank=True,
        null=True,
        related_name='users',
        on_delete=models.SET_NULL,
        verbose_name=_('Organization'))


class FinancialYear(models.Model):
    name = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def get_projects(self):
        return Project.objects.filter(
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        )


class OrganizationFinacialYear(models.Model):
    financial_year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE, related_name='organiaztion_through')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='financial_year_through')
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('financial_year', 'organization',)



# organization info
class Organization(models.Model):
    name = models.TextField()
    logo = models.ImageField(null=True)
    address = models.TextField(null=True)
    city = models.TextField(null=True)
    post_number = models.TextField(null=True)
    tax_number = models.CharField(max_length=10, null=True)
    registration_number = models.TextField(null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    trr = models.TextField(null=True)
    representative = models.TextField(null=True)
    is_charity = models.BooleanField(default=False)
    is_for_the_public_good = models.TextField(default=None, null=True, blank=True)

    financial_years = models.ManyToManyField(FinancialYear, related_name='organizations', through='OrganizationFinacialYear')

    def __str__(self):
        return self.name


class DocumentCategory(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Document(models.Model):
    file = models.FileField()
    category = models.ForeignKey('DocumentCategory', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='documents')
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return f'{self.year.name} - {self.category.name}'


class People(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='people')
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE, related_name='people')
    full_time_employees = models.IntegerField(default=0)
    other_employees = models.IntegerField(default=0)
    volunteers = models.IntegerField(default=0)
    members = models.IntegerField(default=0)
    number_of_men = models.IntegerField(default=0)
    number_of_women = models.IntegerField(default=0)
    number_of_non_binary = models.IntegerField(default=0)
    employees_by_hours = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.year.name} - {self.organization.name}'


class PaymentRatio(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='payment_ratios')
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE, related_name='payment_ratios')

class Employee(models.Model):
    payment_ratio = models.ForeignKey('PaymentRatio', on_delete=models.CASCADE, related_name='employees')
    note = models.TextField()
    average_gross_salary = models.DecimalField(decimal_places=2, max_digits=10)
    job_share = models.IntegerField(
        default=100,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
            ]
        )


# finance

class FinancialCategory(MPTTModel):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='%(class)s_related')
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE,null=True, blank=True, related_name='%(class)s_related')
    name = models.CharField(max_length=256)
    additional_name = models.CharField(max_length=256, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='categories_children')
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    order = models.IntegerField()
    instructions = models.TextField()
    allow_additional_name = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_json_tree(self):
        return {
            'name': self.name,
            'amount': float(self.amount),
            'children': [child.get_json_tree() for child in self.get_children().order_by('order') if child.amount]
        }

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['order']


class RevenueCategory(FinancialCategory):
    pass


class ExpensesCategory(FinancialCategory):
    pass


# projekt

class Project(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='projects')
    name = models.TextField()
    description = MartorField(verbose_name=_('Project\'s description'))
    outcomes_and_impacts = MartorField(verbose_name=_('Project\'s outcomes and impacts'))
    link = models.URLField(null=True, blank=True, verbose_name=_('Project\'s link'))
    value = models.IntegerField()
    organization_share = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def org_share(self):
        return int(self.value * self.organization_share) / 100

    @property
    def icons(self):
        financer_icons = [financer.logo.url for financer in self.financers.all() if financer.logo]
        co_financer_icons = [co_financer.logo.url for co_financer in self.cofinancers.all() if co_financer.logo]
        return financer_icons + co_financer_icons

    @property
    def duration(self):
        r = relativedelta.relativedelta(self.end_date, self.start_date)
        return {
            'days': r.days,
            'months': r.months,
            'years': r.years,
        }


class Financer(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='financers')
    name = models.TextField()
    link = models.URLField(null=True, blank=True, verbose_name='Financer\'s link')
    logo = models.FileField(null=True, blank=True)


class CoFinancer(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='cofinancers')
    name = models.TextField()
    link = models.URLField(null=True, blank=True, verbose_name=_('CoFinancer\'s link'))
    logo = models.FileField(null=True, blank=True)


class Partner(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='partners')
    name = models.TextField()
    link = models.URLField(null=True, blank=True, verbose_name=_('Partners\'s link'))


class Donator(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='donators')
    name = models.TextField()
    link = models.URLField(null=True, blank=True, verbose_name=_('Donators\'s link'))


# donations
class Donations(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='donations')
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT, related_name='donations')
    personal_donations_amount = models.IntegerField(default=0)
    number_of_personal_donations = models.IntegerField(default=0)
    organization_donations_amount = models.IntegerField(default=0)
    number_of_organization_donations = models.IntegerField(default=0)
    one_percent_income_tax = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    purpose_of_donations = MartorField(verbose_name='Donation purpose')

class PersonalDonator(models.Model):
    project = models.ForeignKey('Donations', on_delete=models.CASCADE, related_name='personal_donators')
    name = models.TextField()
    amount = models.IntegerField(default=0)

class OrganiaztionDonator(models.Model):
    project = models.ForeignKey('Donations', on_delete=models.CASCADE, related_name='organiaztion_donators')
    name = models.TextField()
    amount = models.IntegerField(default=0)


# info text

class InfoText(models.Model):
    class CardTypes(models.TextChoices):
        BASICINFO = 'BI', _('BasicInfo')
        PROJECTS = 'PR', _('Projects')
        DONATIONS = 'DO', _('Donations')
        FINANCE = 'FI', _('Finance')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='info_texts')
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT, related_name='info_texts')
    card =  models.CharField(
        max_length=2,
        choices=CardTypes.choices,
        default=CardTypes.BASICINFO,
    )
    text = models.TextField(default='')


# settings
class Instructions(models.Model):
    model = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    list_instructions = MartorField(null=True, blank=True, verbose_name=_('Instructions for list of objects'))
    add_instructions = MartorField(null=True, blank=True, verbose_name=_('Instructions for adding object'))
    edit_instructions = MartorField(null=True, blank=True, verbose_name=_('Instructions for edit single object'))

    def __str__(self):
        if self.model:
            return f'{self.model}'
        else:
            return 'Landing'
