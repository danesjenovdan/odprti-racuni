from functools import partial
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms

from mptt.admin import MPTTModelAdmin


from nvo.models import (Organization, DocumentCategory, Document, People,
    Employee, User, RevenueCategory, ExpensesCategory, FinancialYear, PaymentRatio,
    Project, Financer, CoFinancer, Partner, Donator
)
# Register your models here.


class UserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'organization']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'organization')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )


class LimitedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if not request.user.organization:
            # return empty queryset if user has not organizations
            return qs.model.objects.none()
        return qs.filter(organization=request.user.organization)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'logo'
    ]
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super(OrganizationAdmin, self).get_queryset(request)
        if not request.user.organization:
            return qs
        return qs.filter(id=request.user.organization.id)


# basic info
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]


class DocumentAdmin(LimitedAdmin):
    list_display = [
        'category',
        'year',
        'organization',
    ]


class PeopleAdmin(LimitedAdmin):
    list_display = [
        'year',
        'organization',
    ]


class EmployeeAdmin(admin.TabularInline):
    list_display = [
        'note',
        'average_gross_salary',
        'job_share',
    ]
    model = Employee
    extra = 0


class PaymentRatioAdmin(LimitedAdmin):
    list_display = [
        'year'
    ]
    inlines = [
        EmployeeAdmin,
    ]

class FinanceChangeListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FinanceChangeListForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            if not instance.allow_additional_name:
                self.fields['additional_name'].widget.attrs['hidden'] = 'hidden'


# finance
class FinancialCategoryMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = ['name', 'amount', 'year', 'additional_name']
    list_editable = ['amount', 'additional_name']
    list_filter = ['year']

    def get_list_display_links(self, request, list_display):
        if request.user.is_superuser:
            return ['name']
        else:
            return None

    def get_changelist_form(self, request, **kwargs):
        return FinanceChangeListForm

class RevenueCategoryAdmin(FinancialCategoryMPTTModelAdmin):
    pass

class ExpensesCategoryAdmin(FinancialCategoryMPTTModelAdmin):
    pass


# projects

class FinancerInlineAdmin(admin.TabularInline):
    model = Financer
    extra = 0


class CoFinancerInlineAdmin(admin.TabularInline):
    model = CoFinancer
    extra = 0


class PartnerInlineAdmin(admin.TabularInline):
    model = Partner
    extra = 0


class DonatorInlineAdmin(admin.TabularInline):
    model = Donator
    extra = 0

class ProjectAdmin(LimitedAdmin):
    list_display = [
        'name',
        'year'
    ]
    inlines = [
        FinancerInlineAdmin,
        CoFinancerInlineAdmin,
        PartnerInlineAdmin,
        DonatorInlineAdmin
    ]
    class Media:
        css = {
             'all': ('css/admin-extra.css',)
        }

admin.site.register(RevenueCategory, RevenueCategoryAdmin)
admin.site.register(ExpensesCategory, ExpensesCategoryAdmin)

admin.site.site_header = 'Odprti računi'
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(People, PeopleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(FinancialYear)
admin.site.register(PaymentRatio, PaymentRatioAdmin)
admin.site.register(Project, ProjectAdmin)

