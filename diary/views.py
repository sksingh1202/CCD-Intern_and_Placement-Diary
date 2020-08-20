from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import ModelFormMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms

import datetime

# Create your views here.

class CompanyListView(LoginRequiredMixin, ListView):
    model = models.Company
    fields = ('name', 'POC', 'CPOC', 'additional_POC', 'email', 'logo', 'placement', 'internship')
    template_name = 'diary/company_list.html'

    def get_queryset(self):
        return models.Company.objects.filter(datetime__year=self.kwargs['year'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['yr'] = self.kwargs['year']
        return context

class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = models.Company
    fields = ('name', 'POC', 'CPOC', 'additional_POC', 'email', 'logo', 'placement', 'internship')
    template_name = 'diary/company_create.html'

# you may like to refer: https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-display/#generic-views-of-objects
# to get a better understanding
class CompanyPlacementRemarksListView(LoginRequiredMixin, ListView, ModelFormMixin):
    model = models.Remark
    form_class = forms.RemarkForm
    context_object_name = 'placement_remarks_list'
    template_name = 'diary/company_placement_remarks.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        self.object = self.form.save(commit = False)

        self.object.company = get_object_or_404(models.Company, slug = self.kwargs['slug'], year=self.kwargs['year'])
        self.object.user = request.user
        self.object.placement = True
        self.object.save()
        request.POST = None
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        self.company = get_object_or_404(models.Company, slug = self.kwargs['slug'], placement=True, year=self.kwargs['year'])
        return models.Remark.objects.select_related('company').filter(company=self.company, placement=True, company__datetime__year=self.kwargs['year'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['company'] = self.company
        context['company_placement_hrs'] = models.HR.objects.select_related('company').filter(company=self.company, placement=True)
        if datetime.date.today().year == self.kwargs['year']:
            context['form'] = self.form
        else:
            context['form'] = None
        context['yr'] = self.kwargs['year']
        return context

class CompanyInternRemarksListView(LoginRequiredMixin, ListView, ModelFormMixin):
    model = models.Remark
    form_class = forms.RemarkForm
    context_object_name = 'intern_remarks_list'
    template_name = 'diary/company_intern_remarks.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        self.object = self.form.save(commit = False)

        self.object.company = get_object_or_404(models.Company, slug = self.kwargs['slug'], year = self.kwargs['year'])
        self.object.user = request.user
        self.object.placement = False
        self.object.save()
        request.POST = None
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        self.company = get_object_or_404(models.Company, slug = self.kwargs['slug'], internship=True, year = self.kwargs['year'])
        return models.Remark.objects.select_related('company').filter(company=self.company, placement=False, company__datetime__year=self.kwargs['year'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['company'] = self.company
        context['company_intern_hrs'] = models.HR.objects.select_related('company').filter(company=self.company, internship=True)
        if datetime.date.today().year == self.kwargs['year']:
            context['form'] = self.form
        else:
            context['form'] = None
        context['yr'] = self.kwargs['year']
        return context

class HRCreateView(LoginRequiredMixin, CreateView):
    model = models.HR
    fields = ('name', 'contact_number_1', 'contact_number_2', 'email', 'linkedin_id', 'facebook_id', 'placement', 'internship')
    template_name = 'diary/create_hr.html'

    def form_valid(self, form, **kwargs):
        form.instance.company = get_object_or_404(models.Company, slug = self.kwargs['slug'], year = datetime.date.today().year)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(models.Company, slug = self.kwargs['slug'], year = datetime.date.today().year)
        return context

# class HRNavCreateView(LoginRequiredMixin, CreateView):
#     model = models.HR
#     fields = ('name', 'company', 'contact_number_1', 'contact_number_2', 'email', 'linkedin_id', 'facebook_id', 'placement', 'internship')
#     template_name = 'diary/create_nav_hr.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['company'] = get_object_or_404(models.Company, slug = self.kwargs['slug'])
#         return context
