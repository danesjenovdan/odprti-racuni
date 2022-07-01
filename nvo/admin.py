from django.contrib import admin
from nvo.models import Organization, DocumentCategory, Document, People, Employee
# Register your models here.


class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'logo'
    ]
    search_fields = ['name']


class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]


class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'year',
        'organization',
    ]


class PeopleAdmin(admin.ModelAdmin):
    list_display = [
        'year',
        'organization',
    ]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'year',
        'organization',
        'note',
        'average_gross_salary',
        'job_share',
    ]


admin.site.site_header = 'Odprti računi'
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(People, PeopleAdmin)
admin.site.register(Employee, EmployeeAdmin)

