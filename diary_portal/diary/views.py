from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from . import models

# Create your views here.

class CompanyListView(LoginRequiredMixin, ListView):
    model = models.Company
    fields = ('name', 'POC', 'CPOC', 'additional_POC', 'email', 'logo', 'placement', 'internship')
    template_name = 'diary/company_list.html'

class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = models.Company
    fields = ('name', 'POC', 'CPOC', 'additional_POC', 'email', 'logo', 'placement', 'internship')
    template_name = 'diary/company_create.html'

# you may like to refer: https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-display/#generic-views-of-objects
# to get a better understanding
class CompanyPlacementRemarksListView(LoginRequiredMixin, ListView):
    model = models.Remark
    context_object_name = 'placement_remarks_list'
    template_name = 'diary/company_placement_remarks.html'

    def get_queryset(self):
        self.company = get_object_or_404(models.Company, slug = self.kwargs['slug'])
        return models.Remark.objects.select_related('company').filter(company=self.company, placement=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['company_placement_hrs'] = models.HR.objects.select_related('company').filter(company=self.company, placement=True)
        return context

class CompanyInternRemarksListView(LoginRequiredMixin, ListView):
    model = models.Remark
    context_object_name = 'intern_remarks_list'
    template_name = 'diary/company_intern_remarks.html'

    def get_queryset(self):
        self.company = get_object_or_404(models.Company, slug = self.kwargs['slug'])
        return models.Remark.objects.select_related('company').filter(company=self.company, placement=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['company_intern_hrs'] = models.HR.objects.select_related('company').filter(company=self.company, internship=True)
        return context
