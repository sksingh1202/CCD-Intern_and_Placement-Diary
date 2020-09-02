import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render

from . import forms
from . import models

#api related code


# Create your views here.

class CompanyListView(LoginRequiredMixin, ListView, ModelFormMixin):
    model = models.Company
    form_class = forms.CompanySearch
    # fields = ('name', 'POC', 'CPOC', 'additional_POC', 'email', 'placement', 'internship')
    template_name = 'diary/company_list.html'
    context = None

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        search_text = ""
        return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        return models.Company.objects.filter(datetime__year=self.kwargs['year'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['yr'] = self.kwargs['year']
        context['yr_list'] = [*range(2015, datetime.date.today().year + 1)]
        context['company_list'] = context['object_list']
        # context['logo'] = clearbit.NameToDomain.find(name='Clearbit')['logo']
        # print(context)
        # print(context['yr_list'])
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        self.form = self.get_form(self.form_class)
        search_text = request.POST['search_text']
        if len(search_text):
            self.context['company_list'] = self.context['object_list'].filter(name__icontains=search_text)
        else:
            self.context['company_list'] = self.context['object_list']
        return self.get(request, *args, **kwargs)


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = models.Company
    form_class = forms.CompanyForm
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
        context['yr'] = self.kwargs['year']
        context['yr_list'] = [*range(2015, datetime.date.today().year + 1)]
        if datetime.date.today().year == self.kwargs['year']:
            context['form'] = self.form
        else:
            context['form'] = None
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
        context['yr_list'] = [*range(2015, datetime.date.today().year + 1)]
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

class HRListView(LoginRequiredMixin, ListView):
    model = models.HR
    fields = ('name', 'company', 'contact_number_1', 'contact_number_2', 'email', 'linkedin_id', 'facebook_id', 'placement', 'internship')
    template_name = 'diary/hr_list.html'
    context_object_name = 'hr_list'

    def get_queryset(self):
        self.company = get_list_or_404(models.Company, slug=self.kwargs['slug'])
        return models.HR.objects.select_related('company').filter(company__slug=self.kwargs['slug'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['company_name'] = self.company[0].name
        return context

class HRPresentListView(LoginRequiredMixin, ListView):
    model = models.HR
    fields = ('name', 'company', 'contact_number_1', 'contact_number_2', 'email', 'linkedin_id', 'facebook_id', 'placement', 'internship')
    template_name = 'diary/hr_present_list.html'
    context_object_name = 'hr_present_list'

    def get_queryset(self):
        self.year = datetime.date.today().year
        return models.HR.objects.filter(company__year=self.year)


def error_404_view(requests, exception):
    return render(requests, 'diary/404.html')