from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound

from nvo.models import (Organization, FinancialYear, Document, OrganizationFinancialYear, People, PaymentRatio, RevenueCategory,
    ExpensesCategory, Donations, InfoText)

from nvo.utils import clean_chart_data

def index(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    financial_year_through = organization.financial_year_through.filter(is_active=True).last()
    if financial_year_through:
        return redirect('info', organization_id=organization_id, year=financial_year_through.financial_year.name)
    else:
        return HttpResponseNotFound('')

def organization_basic_info(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    get_object_or_404(
        OrganizationFinancialYear,
        organization=organization,
        financial_year=year,
        is_active=True
    )

    documents = Document.objects.filter(
        year=year,
        organization=organization
    )

    people = get_object_or_404(People, year=year, organization=organization)

    payment_ratio = get_object_or_404(PaymentRatio, year=year, organization=organization)

    info_text = InfoText.objects.filter(year=year, organization=organization, card=InfoText.CardTypes.BASICINFO).first()

    # get donations to decide whether to render the Donations menu item
    donations = get_object_or_404(Donations, year=year, organization=organization)
    
    return render(
        request,
        'basic-info.html',
        {
            'organization': organization,
            'documents': documents,
            'people': people,
            'people_statistics': people.get_statistics(),
            'payment_ratio': payment_ratio.get_statistics(),
            'info_text': info_text,
            'donation': donations,
        })

def get_finance(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    get_object_or_404(
        OrganizationFinancialYear,
        organization=organization,
        financial_year=year,
        is_active=True
    )

    total_income = RevenueCategory.objects.get(year=year, organization=organization, level=0)
    total_expense = ExpensesCategory.objects.get(year=year, organization=organization, level=0)
    revenues = RevenueCategory.objects.filter(year=year, organization=organization, level=1).order_by('order')
    expenses = ExpensesCategory.objects.filter(year=year, organization=organization, level=1).order_by('order')

    info_text = InfoText.objects.filter(year=year, organization=organization, card=InfoText.CardTypes.FINANCE).first()

    revenue_chart_data = clean_chart_data({
        'name': 'revenue',
        'children': [revenue.get_json_tree() for revenue in revenues if revenue.amount]
    })
    expenses_chart_data = clean_chart_data({
        'name': 'expenses',
        'children': [expense.get_json_tree() for expense in expenses if expense.amount]
    })

    # get donations to decide whether to render the Donations menu item
    donations = get_object_or_404(Donations, year=year, organization=organization)

    return render(
        request,
        'finance.html',
        {
            'revenues': [revenue.get_json_tree() for revenue in revenues if revenue.amount],
            'expenses': [expense.get_json_tree() for expense in expenses if expense.amount],
            'total_income': total_income,
            'total_expense': total_expense,
            'other_finances': {
                'volunteers': 45000,
                'partners': 50000,
                'RS_budget': 67000,
                'RS_budget_received_vs_contributed': -22000
            },
            'organization': organization,
            'info_text': info_text,
            'expenses_json': expenses_chart_data,
            'revenue_json': revenue_chart_data,
            'donation': donations,
        })


def get_projects(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    get_object_or_404(
        OrganizationFinancialYear,
        organization=organization,
        financial_year=year,
        is_active=True
    )

    projects = year.get_projects().filter(organization=organization)

    info_text = InfoText.objects.filter(year=year, organization=organization, card=InfoText.CardTypes.PROJECTS).first()

    # get donations to decide whether to render the Donations menu item
    donations = get_object_or_404(Donations, year=year, organization=organization)

    return render(
        request,
        'projects.html',
        {
            'projects': projects,
            'organization': organization,
            'info_text': info_text,
            'donation': donations,
        }
    )


def get_donations(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    get_object_or_404(
        OrganizationFinancialYear,
        organization=organization,
        financial_year=year,
        is_active=True
    )

    donations = get_object_or_404(Donations, year=year, organization=organization)

    info_text = InfoText.objects.filter(year=year, organization=organization, card=InfoText.CardTypes.DONATIONS).first()

    return render(
        request,
        'donations.html',
        {
            'donation': donations,
            'organization': organization,
            'info_text': info_text,
        }
    )
