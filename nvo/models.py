from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

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


class FinancialYear(MPTTModel):
    name = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='none')

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class DocumentCategory(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Document(models.Model):
    file = models.FileField()
    category = models.ForeignKey('DocumentCategory', on_delete=models.PROTECT)
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT)
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT, related_name='documents')

    def __str__(self):
        return f'{self.year.name} - {self.category.name}'


class People(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT)
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT, related_name='people')
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
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT)
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT, related_name='employees')

class Employee(models.Model):
    payment_ratio = models.ForeignKey('PaymentRatio', on_delete=models.CASCADE)
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
    name = models.CharField(max_length=256)
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT)
    additional_name = models.CharField(max_length=256, null=True, blank=True)
    year = models.ForeignKey('FinancialYear', on_delete=models.CASCADE,null=True, blank=True, related_name='%(class)s_related')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='categories_children')
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    order = models.IntegerField()
    instructions = models.TextField()
    allow_additional_name = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['order']


class RevenueCategory(FinancialCategory):
    pass


class ExpensesCategory(FinancialCategory):
    pass
