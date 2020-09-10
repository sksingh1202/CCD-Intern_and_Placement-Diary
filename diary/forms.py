from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime as python_datetime

class CompanyForm(forms.ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            models.Company.objects.get(name=cleaned_data.get('name'), year=python_datetime.date.today().year)
        except models.Company.DoesNotExist:
            pass
        else:
            self.add_error(None, ValidationError(_("This company has already been registered for this year!")))

    class Meta:
        model = models.Company
        fields = ('name', 'POC', 'CPOC', 'additional_POC', 'email', 'placement', 'internship')
        widgets = {
            'name': forms.TextInput(attrs={
                # 'class': 'cla'
                # 'id': <id for this field in html to be used in css>,
                # 'some_other_html_attr': <value_of_that_attribute>
                # PS. Don't forget the comma ',' in between two attributes!
            }),
            'CPOC': forms.CheckboxSelectMultiple(),
        }
        error_messages = {
            'name': {
                'required': _("Please enter the name of the company."),
            },
            'POC': {
                'required': _("Please select a POC for the company."),
            },
            'CPOC': {
                'required': _("Please select a CPOC for the company."),
            },
            'email': {
                'invalid': _("Please enter a valid email address! Example: abc@xyz.com"),
            },
        }

class RemarkForm(forms.ModelForm):
    class Meta:
        model = models.Remark
        fields = ('remark', 'company', 'user', 'placement')
        widgets = {
            'remark': forms.Textarea(attrs={'cols':120, 'rows':5}),
        }
        labels = {
            'remark': _('Add Remark'),
        }
