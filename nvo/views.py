from django.shortcuts import render, get_object_or_404

from nvo.models import Organization, FinancialYear, Document
# Create your views here.

def organization_basic_info(request, organization_id, year):
    organization = get_object_or_404(Organization, pk=organization_id)
    year = get_object_or_404(FinancialYear, name=year)

    documents = Document.objects.filter()

    return render(
        request,
        'basic-info.html',
        {
            'organization': organization,
            'documents': documents
        })
