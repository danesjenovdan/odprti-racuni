from django.urls import path

from nvo.views import (
    get_donations,
    get_export,
    get_finance,
    get_projects,
    index,
    landing,
    organization_basic_info,
)

urlpatterns = [
    path("", landing, name="landing"),
    path("<int:organization_id>/", index, name="index"),
    path(
        "info/<int:organization_id>/leto/<str:year>/",
        organization_basic_info,
        name="info",
    ),
    path("finance/<int:organization_id>/leto/<str:year>/", get_finance, name="finance"),
    path(
        "projekti/<int:organization_id>/leto/<str:year>/", get_projects, name="projects"
    ),
    path(
        "donacije/<int:organization_id>/leto/<str:year>/",
        get_donations,
        name="donations",
    ),
    path("export/<int:organization_id>/<int:year_id>/", get_export, name="export"),
]
