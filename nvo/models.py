from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class FinancialYear(models.Model):
    name = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()


class Organization(models.Model):
    name = models.TextField()
    logo = models.ImageField()
    address = models.TextField()
    city = models.TextField()
    post_number = models.TextField()
    tax_number = models.CharField(max_length=10)
    registration_number = models.TextField()
    email = models.EmailField()
    trr = models.TextField()
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
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.year.name} - {self.category.name}'


class People(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT)
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT)
    full_time_employees = models.IntegerField(default=0)
    other_employees = models.IntegerField(default=0)
    volunteers = models.IntegerField(default=0)
    members = models.IntegerField(default=0)
    employees_by_hours = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.year.name} - {self.organization.name}'


class Employee(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT)
    year = models.ForeignKey('FinancialYear', on_delete=models.PROTECT)
    note = models.TextField()
    average_gross_salary = models.DecimalField(decimal_places=2, max_digits=10)
    job_share = models.IntegerField(
        default=100,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
            ]
        )
