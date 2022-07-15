from django.urls import path

from nvo.views import get_projects, organization_basic_info, get_finance, get_donations

urlpatterns = [
    path('info/<int:organization_id>/leto/<int:year>/', organization_basic_info),
    path('finance/<int:organization_id>/leto/<int:year>/', get_finance),
    path('projekti/<int:organization_id>/leto/<int:year>/', get_projects),
    path('donacije/<int:organization_id>/leto/<int:year>/', get_donations),
]
