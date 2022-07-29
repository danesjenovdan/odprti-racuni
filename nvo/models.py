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



class OrganizationFinacialYear(models.Model):
    financial_year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE, related_name='organiaztion_through', verbose_name=_('Financial year'))
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='financial_year_through', verbose_name=_('Organiaztion'))
    is_active = models.BooleanField(default=False, verbose_name=_('Is active'))

    class Meta:
        unique_together = ('financial_year', 'organization',)

        verbose_name = _('Organiaztion financial year')
        verbose_name_plural = _('Organiaztion financial years')



# organization info
class Organization(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    logo = models.ImageField(null=True, verbose_name=_('Logo'))
    address = models.TextField(null=True, verbose_name=_('Address'))
    city = models.TextField(null=True, verbose_name=_('Post'))
    post_number = models.TextField(null=True, verbose_name=_('Post number'))
    tax_number = models.CharField(max_length=10, null=True, verbose_name=_('TAX number'))
    registration_number = models.TextField(null=True, verbose_name=_('Registration number'))
    email = models.EmailField(null=True, verbose_name=_('Email'))
    phone_number = models.CharField(max_length=13, null=True, blank=True, verbose_name=_('Phone number'))
    trr = models.TextField(null=True, verbose_name=_('TRR'))
    representative = models.TextField(null=True, verbose_name=_('representative'))
    is_charity = models.BooleanField(default=False, verbose_name=_('is charity'))
    is_for_the_public_good = models.TextField(default=None, null=True, blank=True, verbose_name=_('Is organization for public good'))

    financial_years = models.ManyToManyField(FinancialYear, related_name='organizations', through='OrganizationFinacialYear', verbose_name=_('Financial years'))

    def __str__(self):
        return self.name

    def get_years(self):
        return self.financial_years.filter(organiaztion_through__is_active=True).values_list("name", flat=True).order_by("name")

    class Meta:
        verbose_name = _('Organiaztion')
        verbose_name_plural = _('Organization')


class DocumentCategory(models.Model):
    name = models.TextField(verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Document category')
        verbose_name_plural = _('Document categories')


class Document(models.Model):
    file = models.FileField(verbose_name=_('File'))
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
    full_time_employees = models.IntegerField(default=0, verbose_name=_('Full time employees'))
    other_employees = models.IntegerField(default=0, verbose_name=_('Other employees'))
    volunteers = models.IntegerField(default=0, verbose_name=_('Volunteers'))
    members = models.IntegerField(default=0, verbose_name=_('Members'))
    number_of_men = models.IntegerField(default=0, verbose_name=_('Number of men'))
    number_of_women = models.IntegerField(default=0, verbose_name=_('Number of women'))
    number_of_non_binary = models.IntegerField(default=0, verbose_name=_('Number of non binary'))

    def __str__(self):
        return f'{self.year.name} - {self.organization.name}'

    def get_statistics(self):
        num_of_men = self.number_of_men
        num_of_women = self.number_of_women
        num_of_nonbinary = self.number_of_non_binary
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

    class Meta:
        verbose_name = _('Payment ratio')
        verbose_name_plural = _('Payment ratios')


class Employee(models.Model):
    payment_ratio = models.ForeignKey('PaymentRatio', on_delete=models.CASCADE, related_name='employees')
    note = models.TextField(verbose_name=_('Note'))
    average_gross_salary = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_('Average gross selary'))
    job_share = models.IntegerField(
        default=100,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
            ],
        verbose_name=_('job share')
        )

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')


# finance

class FinancialCategory(MPTTModel):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='%(class)s_related', verbose_name=_('Organiaztion'))
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE,null=True, blank=True, related_name='%(class)s_related', verbose_name=_('Year'))
    name = models.CharField(max_length=256, verbose_name=_('Name'))
    additional_name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Additional name'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='categories_children', verbose_name=_('Parent'))
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0, verbose_name=_('Amount'))
    order = models.IntegerField(verbose_name=_('Order'))
    instructions = models.TextField(verbose_name=_('Instructions'))
    allow_additional_name = models.BooleanField(default=False, verbose_name=_('Allow additional name'))

    def __str__(self):
        return self.name + ' ' + self.year.name

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
    name = models.TextField(verbose_name=_('Name'))
    description = MartorField(verbose_name=_('Project\'s description'))
    outcomes_and_impacts = MartorField(verbose_name=_('Project\'s outcomes and impacts'))
    link = models.URLField(null=True, blank=True, verbose_name=_('Project\'s link'))
    value = models.IntegerField(verbose_name=_('Total value'))
    organization_share = models.IntegerField(
        verbose_name=_('Organization share'),
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
            ],
    )
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(verbose_name=_('End date'))

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

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class Financer(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='financers')
    name = models.TextField(verbose_name=_('Name'))
    link = models.URLField(null=True, blank=True, verbose_name='Financer\'s link')
    logo = models.FileField(null=True, blank=True, verbose_name=_('Logo'))

    class Meta:
        verbose_name = _('Financer')
        verbose_name_plural = _('Financers')


class CoFinancer(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='cofinancers')
    name = models.TextField(verbose_name=_('Name'))
    link = models.URLField(null=True, blank=True, verbose_name=_('CoFinancer\'s link'))
    logo = models.FileField(null=True, blank=True, verbose_name=_('Logo'))

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
    personal_donations_amount = models.IntegerField(default=0, verbose_name=_('Personal donation amount'))
    number_of_personal_donations = models.IntegerField(default=0, verbose_name=_('Number of personal donations'))
    organization_donations_amount = models.IntegerField(default=0, verbose_name=_('Organization donations amount'))
    number_of_organization_donations = models.IntegerField(default=0, verbose_name=_('Number od organization donations'))
    one_percent_income_tax = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, verbose_name=_('1 percent income tax'))
    purpose_of_donations = MartorField(verbose_name=_('Donation purpose'))

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
        BASICINFO = 'BI', _('BasicInfo')
        PROJECTS = 'PR', _('Projects')
        DONATIONS = 'DO', _('Donations')
        FINANCE = 'FI', _('Finance')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='info_texts', verbose_name=_('Organization'))
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT, related_name='info_texts', verbose_name=_('Year'))
    card =  models.CharField(
        max_length=2,
        choices=CardTypes.choices,
        default=CardTypes.BASICINFO,
        verbose_name=_('Card')
    )
    text = models.TextField(default='', verbose_name=_('Text'))

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
