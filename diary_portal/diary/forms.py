from django import forms
from . import models
from django.utils.translation import gettext_lazy as _

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
