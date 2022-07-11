from django.urls import path

from nvo.views import organization_basic_info

urlpatterns = [
    path('info/<int:organization_id>/leto/<int:year>/', organization_basic_info),
]
