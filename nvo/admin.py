from functools import partial
from django.contrib import admin
from django.db import models
from django.contrib.admin.apps import AdminConfig
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django import forms

from mptt.admin import MPTTModelAdmin


from nvo.models import (Organization, DocumentCategory, Document, People,
    Employee, User, RevenueCategory, ExpensesCategory, FinancialYear, PaymentRatio,
    Project, Financer, CoFinancer, Partner, Donator, Donations, PersonalDonator,
    OrganiaztionDonator, Instructions, InfoText
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
    exclude = ['organization']
    readonly_fields = ['year']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if not request.user.organization:
            # return empty queryset if user has not organizations
            return qs.model.objects.none()
        return qs.filter(organization=request.user.organization)


class FinancialYearInline(admin.TabularInline):
    readonly_fields = ['financial_year']
    model = Organization.financial_years.through
    extra = 0
    ordering = ("financial_year__name",)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'logo'
    ]
    search_fields = ['name']

    inlines = [
        FinancialYearInline
    ]

    def get_queryset(self, request):
        qs = super(OrganizationAdmin, self).get_queryset(request)
        if not request.user.organization or request.user.is_superuser:
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
    readonly_fields = []

    def save_model(self, request, obj, form, change):
        if not obj.id:
            user = User.objects.get(id=request.user.id)
            organization = user.organization
            obj.organization_id = organization.id
        super().save_model(request, obj, form, change)


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
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows':1, 'cols':40})},
    }


class PaymentRatioAdmin(LimitedAdmin):
    list_display = [
        'year'
    ]
    inlines = [
        EmployeeAdmin,
    ]

# finance
class FinanceChangeListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FinanceChangeListForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            if not instance.allow_additional_name:
                self.fields['additional_name'].widget.attrs['hidden'] = 'hidden'


class FinanceYearListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('By financial year')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'year'
    def __init__(self, request, params, model, model_admin):
        # set default filter
        super().__init__(request, params, model, model_admin)
        last_year_id = request.user.organization.financial_years.last().id
        if self.used_parameters and 'year' in self.used_parameters.keys():
            pass
        else:
            self.used_parameters = {'year': last_year_id}

    def choices(self, changelist):
        value = self.value()
        if not value:
            value = FinancialYear.objects.first().id
        for lookup, title in self.lookup_choices:
            yield {
                'selected': str(value) == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }


    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            years = FinancialYear.objects.all()
        else:
            years = request.user.organization.financial_years.all()
        return (
            (year.id, year.name) for year in years
        )

    def queryset(self, request, queryset):
        return queryset.filter(year_id=self.value())

class FinacialFormSet(forms.BaseModelFormSet):
    """
    This formset is used for validate amounts in finance admin view
    """
    def clean(self):
        form_set = self.cleaned_data
        root_node = form_set[0]['id']

        # create pairs from formset {node_id: node_amount, ...}
        self.enumerated_amounts = {
            node['id'].id: node['amount'] for node in form_set
        }
        self.clean_branch(root_node)

        return form_set

    def clean_branch(self, root_node):
        children = root_node.get_children()
        if children:
            # get node amount from formset
            childen_amount = sum([self.enumerated_amounts[child.id] for child in children])
            root_amount = self.enumerated_amounts[root_node.id]
            if root_amount != childen_amount:
                raise forms.ValidationError(_('Item amount of ') + root_node.name + _(' and its children is not valid.') + f'{root_amount} != {childen_amount}')
            for child in children:
                self.clean_branch(child)


class FinancialCategoryMPTTModelAdmin(LimitedAdmin, MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = ['name', 'amount', 'year', 'additional_name']
    list_editable = ['amount', 'additional_name']
    list_filter = [FinanceYearListFilter]

    def get_list_display_links(self, request, list_display):
        if request.user.is_superuser:
            return ['name']
        else:
            return None

    def get_changelist_form(self, request, **kwargs):
        return FinanceChangeListForm

    def get_changelist_formset(self, request, **kwargs):
        kwargs['formset'] = FinacialFormSet
        changelist_formset = super().get_changelist_formset(request, **kwargs)
        return changelist_formset

class RevenueCategoryAdmin(FinancialCategoryMPTTModelAdmin):
    pass

class ExpensesCategoryAdmin(FinancialCategoryMPTTModelAdmin):
    pass


# projects

class FinancerInlineAdmin(admin.TabularInline):
    model = Financer
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows':1, 'cols':40})},
    }


class CoFinancerInlineAdmin(admin.TabularInline):
    model = CoFinancer
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows':1, 'cols':40})},
    }


class PartnerInlineAdmin(admin.TabularInline):
    model = Partner
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows':1, 'cols':40})},
    }


class DonatorInlineAdmin(admin.TabularInline):
    model = Donator
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows':1, 'cols':40})},
    }


class ProjectYearListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('By financial year')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = request.user.organization.financial_years.all()
        return [(year.id, year.name) for year in years]

    def queryset(self, request, queryset):
        if self.value():
            year = FinancialYear.objects.get(id=self.value())
            this_year_projects = year.get_projects()
            queryset = queryset.filter(id__in=this_year_projects)
            return queryset
        else:
            return queryset

class ProjectAdmin(LimitedAdmin):
    readonly_fields = []
    list_display = [
        'name',
        'start_date',
        'end_date',
    ]
    list_filter = [ProjectYearListFilter]
    inlines = [
        FinancerInlineAdmin,
        CoFinancerInlineAdmin,
        PartnerInlineAdmin,
        DonatorInlineAdmin
    ]

    def save_model(self, request, obj, form, change):
        if not obj.id:
            user = User.objects.get(id=request.user.id)
            organization = user.organization
            obj.organization_id = organization.id
        super().save_model(request, obj, form, change)

    class Media:
        css = {
             'all': ('css/admin-extra.css',)
        }


class PersonalDonatorInlineAdmin(admin.TabularInline):
    model = PersonalDonator
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows':1, 'cols':40})},
    }


class OrganiaztionDonatorInlineAdmin(admin.TabularInline):
    model = OrganiaztionDonator
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows':1, 'cols':40})},
    }


class DonationsAdmin(LimitedAdmin):
    list_display = [
        'year'
    ]
    inlines = [
        PersonalDonatorInlineAdmin,
        OrganiaztionDonatorInlineAdmin
    ]

    class Media:
        css = {
             'all': ('css/admin-extra.css',)
        }

class InstructionsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # TODO
        # if Instructions.objects.filter(model=obj.model):
        #     messages.add_message(request, messages.ERROR, 'Instrucations for this model alredy exists')
        # else:
        super().save_model(request, obj, form, change)


class InfoTextAdmin(LimitedAdmin):
    list_display = [
        'year',
        'card'
    ]
    list_filter = ['year']
    readonly_fields = ['year', 'card']
    exclude = ['organization']



class AdminSite(admin.AdminSite):
    site_header = _('Odprti računi')
    def __init__(self, *args, **kwargs):
        super(AdminSite, self).__init__(*args, **kwargs)
        self._registry.update(admin.site._registry)

    def each_context(self, request):
        url_attrs = []

        # show misisng data as error
        try:
            organization = request.user.organization
        except:
            organization = None
        if organization:
            for financial_year_through in organization.financial_year_through.filter(is_active=True):
                if not Document.objects.filter(organization=organization, year=financial_year_through.financial_year):
                    messages.add_message(request, messages.WARNING, _('You need add at least one document for financial year ') + financial_year_through.financial_year.name)

        context = super().each_context(request)

        # insert instructions

        url_name = request.resolver_match.url_name
        url_attrs = url_name.split('_')

        instructions = ''
        if len(url_attrs) == 1:
            instructions = Instructions.objects.filter(model=None)
            if instructions:
                instructions = instructions[0].list_instructions
            else:
                instructions = ''
        elif len(url_attrs) == 3:
            instructions = Instructions.objects.filter(
                model__model__iexact=url_attrs[1]
            )
            if instructions:
                if url_attrs[2] == 'change':
                    instructions = instructions[0].edit_instructions
                elif url_attrs[2] == 'add':
                    instructions = instructions[0].add_instructions
                else:
                    instructions = instructions[0].list_instructions
            else:
                instructions = ''

        context.update({
            "instructions": instructions,
        })
        return context

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "Skupine": 1,
            "Finančna leta": 2,
            "Uporabniki": 3,
            "Navodila": 4,
            "Kategorije dokumentov": 5,
            "Organizacija": 6,
            "Ljudje": 7,
            "Plačilna razmerja": 8,
            "Dokumenti": 9,
            "Donacije": 10,
            "Odhodki": 11,
            "Prihodki": 12,
            "Projekt": 13,
            "Info texti": 14,
        }

        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            delete_idx = []
            app['models'].sort(key=lambda x: ordering[x['name']])
            if not request.user.is_superuser:
                for idx, model in enumerate(app['models']):
                    # find indexes of models for remove
                    if model['name'] in ['Finančna leta', 'Kategorije dokumentov']:
                        app['models'].remove(model)
                        delete_idx.append(idx)
                    # add id of users organization to organiaztion url
                    if model['name'] == 'Organizacija':
                        user_organization_id = request.user.organization_id
                        model['admin_url'] = model['admin_url'] + str(user_organization_id)
            # delete models from list for Nvo users
            for idx in reversed(delete_idx):
                app['models'].pop(idx)
        return app_list

admin_site = AdminSite(name='Odprti računi')

admin_site.register(RevenueCategory, RevenueCategoryAdmin)
admin_site.register(ExpensesCategory, ExpensesCategoryAdmin)
admin_site.register(Organization, OrganizationAdmin)
admin_site.register(DocumentCategory, DocumentCategoryAdmin)
admin_site.register(Document, DocumentAdmin)
admin_site.register(People, PeopleAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(FinancialYear)
admin_site.register(PaymentRatio, PaymentRatioAdmin)
admin_site.register(Project, ProjectAdmin)
admin_site.register(Donations, DonationsAdmin)
admin_site.register(Instructions, InstructionsAdmin)
admin_site.register(InfoText, InfoTextAdmin)
admin.site = admin_site
