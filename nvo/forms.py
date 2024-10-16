from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from nvo.models import Organization, Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"

    # The clean method gets invoked before the NoteAdmin's save_model method
    def clean(self):
        value = self.cleaned_data.get("value", None)
        organization_share = self.cleaned_data.get("organization_share", None)
        self_money = self.cleaned_data.get("self_money", None)
        start_date = self.cleaned_data.get("start_date", None)
        end_date = self.cleaned_data.get("end_date", None)
        if organization_share and value and organization_share > value:
            raise ValidationError(
                _(
                    "Delež organizacije od celotnega projekta je večji kot vrednost celotnega projekta."
                )
            )

        if self_money and value and self_money > value:
            raise ValidationError(
                _("Lastni vložek je večji kot vrednost celotnega projekta.")
            )

        if start_date and end_date and start_date > end_date:
            raise ValidationError(
                _(
                    "Datum začetka projekta je trenutno nastavljen po datumu, ki je določen za konec projekta. Preverite pravilnost datumov in jih ustrezno uredite."
                )
            )


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        widgets = {
            "name": forms.widgets.Textarea(attrs={"cols": 32, "rows": 1}),
            "post_number": forms.widgets.Textarea(attrs={"cols": 32, "rows": 1}),
            "representative": forms.widgets.Textarea(attrs={"cols": 32, "rows": 1}),
            "address": forms.widgets.Textarea(attrs={"cols": 32, "rows": 3}),
            "registration_number": forms.widgets.Textarea(
                attrs={"cols": 32, "rows": 1}
            ),
            "trr": forms.widgets.Textarea(attrs={"cols": 32, "rows": 1}),
            "is_for_the_public_good": forms.widgets.Textarea(
                attrs={"cols": 32, "rows": 3}
            ),
        }
        fields = "__all__"


class FinanceChangeListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FinanceChangeListForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance:
            if not instance.allow_additional_name:
                self.fields["additional_name"].widget.attrs["hidden"] = "hidden"
