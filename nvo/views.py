from django.shortcuts import render, get_object_or_404

from nvo.models import (Organization, FinancialYear, Document, People, PaymentRatio, RevenueCategory,
    ExpensesCategory, Donations, InfoText)
# Create your views here.

def organization_basic_info(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    documents = Document.objects.filter(year=year)

    people = get_object_or_404(People, year=year, organization=organization)

    payment_ratio = get_object_or_404(PaymentRatio, year=year, organization=organization)

    info_text = InfoText.objects.filter(year=year, organization=organization, card=InfoText.CardTypes.BASICINFO).first()

    return render(
        request,
        'basic-info.html',
        {
            'organization': organization,
            'documents': documents,
            'people': people.get_statistics(),
            'payment_ratio': payment_ratio.get_statistics(),
            'info_text': info_text,
        })

def get_finance(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    revenues = RevenueCategory.objects.filter(year=year, organization=organization, level=0).order_by('order')
    expenses = ExpensesCategory.objects.filter(year=year, organization=organization, level=0).order_by('order')

    info_text = InfoText.objects.filter(year=year, organization=organization, card=InfoText.CardTypes.FINANCE).first()

    return render(
        request,
        'finance.html',
        {
            'revenues': [revenue.get_json_tree() for revenue in revenues if revenue.amount],
            'expenses': [expense.get_json_tree() for expense in expenses if expense.amount],
            'organization': organization,
            'info_text': info_text,
        })


def get_projects(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    projects = year.get_projects().filter(organization=organization)

    info_text = InfoText.objects.filter(year=year, organization=organization, card=InfoText.CardTypes.PROJECTS).first()

    return render(
        request,
        'projects.html',
        {
            'projects': projects,
            'organization': organization,
            'info_text': info_text,
        }
    )


def get_donations(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

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
