from django.shortcuts import render, get_object_or_404, get_list_or_404

from nvo.models import (Organization, FinancialYear, Document, People, PaymentRatio, Project, RevenueCategory,
    ExpensesCategory)
# Create your views here.

def organization_basic_info(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    documents = Document.objects.filter()

    people = get_object_or_404(People, year=year, organization=organization)
    num_of_men = people.number_of_men
    num_of_women = people.number_of_women
    num_of_nonbinary = people.number_of_non_binary
    all_people = num_of_men + num_of_women + num_of_nonbinary
    people = {
        'men': round(num_of_men * 100 / all_people, 2),
        'women': round(num_of_women * 100 / all_people, 2),
        'nonbinary': round(num_of_nonbinary * 100 / all_people, 2)
    }

    payment_ratio = get_object_or_404(PaymentRatio, year=year, organization=organization)
    employees = payment_ratio.employees.all()
    normalized_salaries = [employee.average_gross_salary / employee.job_share * 100 for employee in employees]
    average = sum(normalized_salaries) / len(normalized_salaries)
    min_salary = min(normalized_salaries)
    max_salary = max(normalized_salaries)

    payment_ratio = {
        'highest_absolute': round(max_salary / min_salary, 2),
        'lowest': 1,
        'highest': round(max_salary / average, 2),
        'average': 1
    }

    return render(
        request,
        'basic-info.html',
        {
            'organization': organization,
            'documents': documents,
            'people': people,
            'payment_ratio': payment_ratio
        })

def get_finance(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    revenues = RevenueCategory.objects.filter(year=year, organization=organization, level=0).order_by('order')
    expenses = ExpensesCategory.objects.filter(year=year, organization=organization, level=0).order_by('order')

    return render(
        request,
        'finance.html',
        {
            'revenues': [revenue.get_json_tree() for revenue in revenues if revenue.amount],
            'expenses': [expense.get_json_tree() for expense in expenses if expense.amount],
        })


def get_projects(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    projects = Project.objects.filter(year=year, organization=organization)
    print(projects[0].icons)
    return render(
        request,
        'projects.html',
        {
            'projects': projects,
        }
    )
