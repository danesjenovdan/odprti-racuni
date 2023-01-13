from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from mptt.models import MPTTModel, TreeForeignKey
from martor.models import MartorField
from dateutil import relativedelta
from datetime import timedelta

from nvo.behaviors.models import Timestampable
from django.core.exceptions import ValidationError
import os


def document_size_validator(value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Datoteka je prevelika. Največja možna velikost je 10 MB.')

def image_validator(image):
    limit = 1 * 1024 * 1024
    if image.size > limit:
        raise ValidationError('Slika je prevelika. Največja možna velikost je 1 MB.')

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Format slike ni med podprtimi formati. Podprti formati so jpg in png.')

# MODELS

class User(AbstractUser, Timestampable):
    organization = models.ForeignKey(
        'Organization',
        blank=True,
        null=True,
        related_name='users',
        on_delete=models.SET_NULL,
        verbose_name=_('Organization'))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class FinancialYear(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(verbose_name=_('End date'))

    def __str__(self):
        return self.name

    def get_projects(self):
        return Project.objects.filter(
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        )

    class Meta:
        verbose_name = _('Financial year')
        verbose_name_plural = _('Financial years')
        ordering = ['name']



class OrganizationFinancialYear(models.Model):
    financial_year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE, related_name='organiaztion_through', verbose_name=_('Financial year'))
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='financial_year_through', verbose_name=_('Organiaztion'))
    embed = models.ForeignKey('Embed', on_delete=models.CASCADE, null=True, related_name='financial_year_through', verbose_name=_('Embed'))
    is_active = models.BooleanField(default=False, verbose_name=_('Is active'))

    class Meta:
        unique_together = ('financial_year', 'organization',)

        verbose_name = _('Organiaztion financial year')
        verbose_name_plural = _('Organiaztion financial years')



# organization info
class Organization(models.Model):
    name = models.TextField(verbose_name=_('Organization name'))
    logo = models.ImageField(
        null=True,
        verbose_name=_('Logo'),
        validators=[image_validator, validate_image_extension])
    link = models.URLField(null=True, blank=True, verbose_name=_('Organization\'s link'))
    address = models.TextField(null=True, verbose_name=_('Address'))
    post_number = models.TextField(null=True, verbose_name=_('Post number'))
    tax_number = models.CharField(max_length=10, null=True, verbose_name=_('TAX number'))
    registration_number = models.TextField(null=True, verbose_name=_('Registration number'))
    email = models.EmailField(null=True, verbose_name=_('Email'))
    phone_number = models.CharField(max_length=13, null=True, blank=True, verbose_name=_('Phone number'))
    trr = models.TextField(null=True, verbose_name=_('TRR'))
    representative = models.TextField(null=True, verbose_name=_('representative'))
    is_charity = models.BooleanField(default=False, verbose_name=_('is charity'))
    is_for_the_public_good = models.TextField(default=None, null=True, blank=True, verbose_name=_('Is organization for public good'))

    financial_years = models.ManyToManyField(FinancialYear, related_name='organizations', through='OrganizationFinancialYear', verbose_name=_('Financial years'))

    def __str__(self):
        return self.name

    def get_years(self):
        return self.financial_years.filter(organiaztion_through__is_active=True).values_list("name", flat=True).order_by("name")

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organization')


class DocumentCategory(models.Model):
    name = models.TextField(verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Document category')
        verbose_name_plural = _('Document categories')


class Document(models.Model):
    file = models.FileField(
        verbose_name=_('File'),
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'xls']),
            document_size_validator
        ]
    )
    category = models.ForeignKey('DocumentCategory', on_delete=models.CASCADE, verbose_name=_('Category'))
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='documents', verbose_name=_('Organiaztion'))
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE, related_name='documents', verbose_name=_('Year'))

    def __str__(self):
        return f'{self.year.name} - {self.category.name}'

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')


class People(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='people', verbose_name=_('Organiaztion'))
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE, related_name='people', verbose_name=_('Year'))
    full_time_employees = models.IntegerField(null=True, verbose_name=_('Full time employees'))
    other_employees = models.IntegerField(null=True, verbose_name=_('Other employees'))
    volunteers = models.IntegerField(verbose_name=_('Volunteers'), null=True, blank=True)
    members = models.IntegerField(verbose_name=_('Members'), null=True, blank=True)
    number_of_men = models.IntegerField(null=True, verbose_name=_('Number of men'))
    number_of_women = models.IntegerField(null=True, verbose_name=_('Number of women'))
    number_of_non_binary = models.IntegerField(null=True, verbose_name=_('Number of non binary'))

    def __str__(self):
        return f'{_("People")} {self.year}'

    def get_statistics(self):
        num_of_men = self.number_of_men or 0
        num_of_women = self.number_of_women or 0
        num_of_nonbinary = self.number_of_non_binary or 0
        all_people = num_of_men + num_of_women + num_of_nonbinary
        if all_people == 0:
            return {}
        else:
            return {
                'men': round(num_of_men * 100 / all_people, 2),
                'women': round(num_of_women * 100 / all_people, 2),
                'nonbinary': round(num_of_nonbinary * 100 / all_people, 2)
            }

    class Meta:
        verbose_name = _('People')
        verbose_name_plural = _('People')


class PaymentRatio(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='payment_ratios', verbose_name=_('Organiaztion'))
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE, related_name='payment_ratios', verbose_name=_('Year'))

    def get_statistics(self):
        employees = self.employees.all()
        normalized_salaries = [employee.average_gross_salary / employee.job_share * 100 for employee in employees]
        if normalized_salaries == []:
            return {}
        else:
            average = sum(normalized_salaries) / len(normalized_salaries)
            min_salary = min(normalized_salaries)
            max_salary = max(normalized_salaries)

            return {
                'highest_absolute': round(max_salary / min_salary, 2),
                'lowest': 1,
                'highest': round(max_salary / average, 2),
                'average': 1
            }

    def __str__(self):
        return f'{_("Payment ratio")} {self.year}'

    class Meta:
        verbose_name = _('Payment ratio')
        verbose_name_plural = _('Payment ratios')


class Employee(models.Model):
    payment_ratio = models.ForeignKey('PaymentRatio', on_delete=models.CASCADE, related_name='employees')
    note = models.TextField(verbose_name=_('Note'))
    average_gross_salary = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_('Average gross selary'))
    job_share = models.IntegerField(
        null=True,
        validators=[
            MinValueValidator(1)
            ],
        verbose_name=_('job share')
        )

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')


# finance

class Finance(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='finances', verbose_name=_('Organiaztion'))
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE,null=True, related_name='finances', verbose_name=_('Year'))
    amount_voluntary_work = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, verbose_name=_('Amount of voluntary work'))
    payments_project_partners = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, verbose_name=_('Payments to projects partners'))
    payment_state_budget = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, verbose_name=_('Payment to the state budget'))
    acquired_state_budget = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, verbose_name=_('Difference payment state budget'))

    @property
    def difference_state_budget(self):
        if self.payment_state_budget and self.acquired_state_budget:
            return self.acquired_state_budget - self.payment_state_budget
        else:
            return 0

    def __str__(self):
        return f'{_("Finance")} {self.year.name}'

    class Meta:
        verbose_name = _('Finance')
        verbose_name_plural = _('Finance')


class FinancialCategory(MPTTModel):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='%(class)s_related', verbose_name=_('Organiaztion'))
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE,null=True, blank=True, related_name='%(class)s_related', verbose_name=_('Year'))
    name = models.CharField(max_length=256, verbose_name=_('Name'))
    additional_name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Additional name'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='categories_children', verbose_name=_('Parent'))
    amount = models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name=_('Amount'))
    order = models.IntegerField(verbose_name=_('Order'))
    instructions = models.TextField(verbose_name=_('Instructions'))
    allow_additional_name = models.BooleanField(default=False, verbose_name=_('Allow additional name'))

    def __str__(self):
        return self.name + ' ' + self.year.name

    def get_json_tree(self):
        return {
            'name': self.name,
            'amount': float(self.amount),
            'additional_name': self.additional_name,
            'children': [child.get_json_tree() for child in self.get_children().order_by('order') if child.amount]
        }

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['order']


class RevenueCategory(FinancialCategory):
    class Meta:
        verbose_name = _('Revenue')
        verbose_name_plural = _('Revenues')


class ExpensesCategory(FinancialCategory):
    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')


# projekt

class Project(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='projects', verbose_name=_('Organization'))
    name = models.TextField(verbose_name=_('Project name'))
    description = MartorField(verbose_name=_('Project\'s description'))
    outcomes_and_impacts = MartorField(verbose_name=_('Project\'s outcomes and impacts'))
    link = models.URLField(null=True, blank=True, verbose_name=_('Project\'s link'))
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Total value'))
    self_money = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, verbose_name=_('Self money'))
    organization_share = models.DecimalField(
        verbose_name=_('Organization share'),
        validators=[
            MinValueValidator(1)
            ],
        max_digits=10,
        decimal_places=2,
    )
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(verbose_name=_('End date'))

    @property
    def org_share(self):
        return int(self.value * self.organization_share) / 100

    @property
    def icons(self):
        financer_icons = [financer.logo for financer in self.financers.all() if financer.logo]
        co_financer_icons = [co_financer.logo for co_financer in self.cofinancers.all() if co_financer.logo]
        return financer_icons + co_financer_icons

    def icon_urls(self):
        return [icon.url for icon in self.icons]

    @property
    def duration(self):
        r = relativedelta.relativedelta(self.end_date+timedelta(days=1), self.start_date)
        return {
            'days': r.days,
            'months': r.months + r.years * 12,
        }

    def __str__(self):
        return f''

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class Financer(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='financers')
    name = models.TextField(verbose_name=_('Name'))
    link = models.URLField(null=True, blank=True, verbose_name='Povezava do spletnega mesta')
    logo = models.ImageField(
        null=True,
        blank=True,
        verbose_name=_('Logo'),
        validators=[image_validator, validate_image_extension]
    )

    class Meta:
        verbose_name = _('Financer')
        verbose_name_plural = _('Financers')


class CoFinancer(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='cofinancers')
    name = models.TextField(verbose_name=_('Name'))
    link = models.URLField(null=True, blank=True, verbose_name=_('CoFinancer\'s link'))
    logo = models.ImageField(
        null=True,
        blank=True,
        verbose_name=_('Logo'),
        validators=[image_validator, validate_image_extension]
    )

    class Meta:
        verbose_name = _('Cofinancer')
        verbose_name_plural = _('Cofinancers')


class Partner(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='partners')
    name = models.TextField(verbose_name=_('Name'))
    link = models.URLField(null=True, blank=True, verbose_name=_('Partners\'s link'))

    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')


class Donator(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='donators')
    name = models.TextField(verbose_name=_('Name'))
    link = models.URLField(null=True, blank=True, verbose_name=_('Donators\'s link'))

    class Meta:
        verbose_name = _('Donator')
        verbose_name_plural = _('Donators')


# donations
class Donations(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='donations', verbose_name=_('Organization'))
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT, related_name='donations', verbose_name=_('Year'))
    personal_donations_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, verbose_name=_('Personal donation amount'))
    number_of_personal_donations = models.IntegerField(null=True, blank=True, verbose_name=_('Number of personal donations'))
    organization_donations_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, verbose_name=_('Organization donations amount'))
    number_of_organization_donations = models.IntegerField(null=True, blank=True, verbose_name=_('Number od organization donations'))
    one_percent_income_tax = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, verbose_name=_('1 percent income tax'))
    purpose_of_donations = models.TextField(null=True, blank=True, verbose_name=_('Donation purpose'))

    def __str__(self):
        return self.year.name

    class Meta:
        verbose_name = _('Donations')
        verbose_name_plural = _('Donations')


class PersonalDonator(models.Model):
    project = models.ForeignKey('Donations', on_delete=models.CASCADE, related_name='personal_donators')
    name = models.TextField(verbose_name=_('Name'))
    amount = models.IntegerField(default=0, verbose_name=_('Amount'))

    class Meta:
        verbose_name = _('PersonalDonator')
        verbose_name_plural = _('PersonalDonators')


class OrganiaztionDonator(models.Model):
    project = models.ForeignKey('Donations', on_delete=models.CASCADE, related_name='organiaztion_donators')
    name = models.TextField(verbose_name=_('Name'))
    amount = models.IntegerField(default=0, verbose_name=_('Amount'))

    class Meta:
        verbose_name = _('OrganiaztionDonator')
        verbose_name_plural = _('OrganiaztionDonators')


# info text

class InfoText(models.Model):
    class CardTypes(models.TextChoices):
        # basic info
        BASICINFO = 'BI', _('BasicInfo')
        YEARLYREPORTS = 'YR', _('Documents')
        PEOPLE = 'PE', _('People')
        PAYMENTRATIOS = 'PS', _('Payment ratios')
        # projects
        PROJECTS = 'PR', _('Projects')
        # donations
        PERSONAL_DONATIONS = 'DO', _('Personal donation')
        ORG_DONATIONS = 'OD', _('Organizatin donations')
        INCOME_TAX = 'IT', _('1 percent income tax')
        DONATION_CONSUMPTION = 'DC', _('Donation purpose')
        # finance
        REVENUE = 'FI', _('Revenue')
        EXPENSE = 'EX', _('Expanse')
        VOLUNTIER = 'CO', _('Amount of voluntary work')
        PRO_PARTNERS = 'PP', _('Payments to projects partners')
        STATE_BUDGET = 'SB', _('Payment to the state budget')

    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='info_texts', verbose_name=_('Organization'))
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT, related_name='info_texts', verbose_name=_('Year'))
    card =  models.CharField(
        max_length=2,
        choices=CardTypes.choices,
        default=CardTypes.BASICINFO,
        verbose_name=_('Card')
    )
    pre_text = models.TextField(default='', verbose_name=_('Description'))
    text = models.TextField(default='', blank=True, verbose_name=_('Text'))

    def __str__(self):
        return f'{self.year}'

    class Meta:
        verbose_name = _('Info Text')
        verbose_name_plural = _('Info Texts')


# settings
class Instructions(models.Model):
    model = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Model'))
    list_instructions = MartorField(null=True, blank=True, verbose_name=_('Instructions for list of objects'))
    add_instructions = MartorField(null=True, blank=True, verbose_name=_('Instructions for adding object'))
    edit_instructions = MartorField(null=True, blank=True, verbose_name=_('Instructions for edit single object'))

    def __str__(self):
        if self.model:
            return f'{self.model}'
        else:
            return 'Landing'

    class Meta:
        verbose_name = _('Instructions')
        verbose_name_plural = _('Instructions')


class Embed(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='embeds', verbose_name=_('Organization'))
    def __str__(self):
        return ''
    class Meta:
        verbose_name = _('Koda za vdelavo')
        verbose_name_plural = _('Koda za vdelavo')
