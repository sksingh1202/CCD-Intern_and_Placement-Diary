from django import forms
from . import models
from django.utils.translation import gettext_lazy as _

class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ('name', 'POC', 'CPOC', 'additional_POC', 'email', 'placement', 'internship')
        widgets = {
            'CPOC': forms.CheckboxSelectMultiple(),
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
