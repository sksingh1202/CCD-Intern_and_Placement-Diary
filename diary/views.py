import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, get_list_or_404, render,redirect
from django.views.generic.edit import CreateView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from . import forms
from . import models
from .forms import TodoForm ,Todo1Form
from .models import Todo,Todo1,activities ,Company
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from .signals import new_task,new_task1,intern_task_delete,intern_task_delete2,new_company

# this is a global variable which represents the year version of the current company_list page:
GLOBAL_YR = 0
# Create your views here.

class CompanyListView(LoginRequiredMixin, ListView):
    model = models.Company
    fields = ('name', 'POC', 'CPOC', 'additional_POC', 'email', 'placement', 'internship')
    template_name = 'diary/company_list.html'

    def get_queryset(self):
        return models.Company.objects.filter(datetime__year=self.kwargs['year'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['yr'] = self.kwargs['year']
        global GLOBAL_YR
        GLOBAL_YR = self.kwargs['year']
        print(datetime.date.today().year)
        context['yr_list'] = [*range(2015, datetime.date.today().year + 1)]
        return context

def company_update(request, *args, **kwargs):
    global GLOBAL_YR
    context = {'company_list':models.Company.objects.filter(datetime__year=GLOBAL_YR), 'yr':GLOBAL_YR}
    if request.method == "POST" and len(str(request.POST.get('search_text'))):
        context['company_list'] = models.Company.objects.filter(datetime_year=GLOBAL_YR, name_icontains=request.POST.get("search_text"))
    return render(request, "diary/_filtered_companies.html", context)

def company_intern_placement_filter(request, *args, **kwargs):
    global GLOBAL_YR
    context = {'company_list':models.Company.objects.filter(datetime__year=GLOBAL_YR), 'yr':GLOBAL_YR}
    if request.method == "POST" and request.POST.get("all_val") == "False":
        context['company_list'] =  models.Company.objects.filter(datetime__year=GLOBAL_YR, placement=(request.POST.get("place_val") == "True"), internship=(request.POST.get("intern_val") == "True"))
    return render(request, "diary/_filtered_companies.html", context)

class CompanyCreateView(LoginRequiredMixin, CreateView, ModelFormMixin):
    model = models.Company
    form_class = forms.CompanyForm
    template_name = 'diary/company_create.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return CreateView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        self.object = self.form.save(commit = False)
        self.object.user = request.user
        self.object.save()
        request.POST = None
        # print(self.object)
        # return self.get(request, *args, **kwargs)
        return redirect('/companies/' + str(datetime.date.today().year))
        # return self.object.get_absolute_url()

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
    form_class = forms.HRForm
    template_name = 'diary/create_hr.html'

    # to check whether company has registered for the present year.
    # it is to be done manually because the company field in hrs model is not in the form so there is no validation done by django
    # in this regard.
    # form.instance is an instance of the model(whose values of fields are that of entered by user) not saved yet as a form!
    # we can use it to modify data before creating a row in db or to add values to some fields which were not displayed while taking input
    # def form_valid(self, form, **kwargs):
    #     form.instance.company = get_object_or_404(models.Company, slug = self.kwargs['slug'], year = datetime.date.today().year)
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(models.Company, slug = self.kwargs['slug'], year = datetime.date.today().year)
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return CreateView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        self.object = self.form.save(commit = False)
        self.object.user = request.user
        self.object.company = get_object_or_404(models.Company, slug = self.kwargs['slug'], year = datetime.date.today().year)
        self.object.save()
        request.POST = None
        # return self.get(request, *args, **kwargs)
        return redirect('/hr/' + str(datetime.date.today().year))

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

@login_required
def intern_calendar(request): 
  
    item_list = Todo.objects.order_by("-date") 
    if request.method == "POST": 
        form = TodoForm(request.POST) 
        if form.is_valid():
            form_temp = form.save(commit=False)
            form_temp.username = request.user
            form.save()
            return HttpResponseRedirect(reverse_lazy('intern_calendar'))
            
            
    form = TodoForm()
    page = { 
             "forms" : form, 
             "list" : item_list, 
             "title" : "TODO LIST", 
            
           } 
    return render(request,'diary/intern_calendar.html' , page)
    # return render(request,'diary/intern_calendar.html') 
  
  
  
### function to remove item, it recive todo item id from url ## 
@login_required
def remove(request, item_id): 
    item = Todo.objects.get(pk=item_id) 
    if item.username == request.user:
        intern_task_delete.send(sender=Todo, Todo=item)
        item.delete()
        messages.info(request, "item removed !!!")  
        return redirect('/intern_calendar')
    else:
        return redirect('/404.html')

@login_required
def placement_calendar(request): 
  
    item_list = Todo1.objects.order_by("-date") 
    if request.method == "POST": 
        form = Todo1Form(request.POST) 
        if form.is_valid():
            form_temp = form.save(commit=False)
            form_temp.username = request.user
            form.save()
            return HttpResponseRedirect(reverse_lazy('placement_calendar'))
            
            
    form = Todo1Form()
    page = { 
             "forms" : form, 
             "list" : item_list, 
             "title" : "TODO LIST", 
            
           } 
    return render(request,'diary/placement_calendar.html' , page)

@login_required
def remove1(request, item1_id): 
    item1 = Todo1.objects.get(pk=item1_id) 
    if item1.username == request.user:
        intern_task_delete2.send(sender=Todo1, Todo1=item1)
        item1.delete()
        messages.info(request, "item removed !!!")  
        return redirect('/placement_calendar')
    else:
        return redirect('/404.html')

@login_required
def user_intern_calendar(request,username):
    item_list = Todo.objects.filter(username__username=username).order_by('-date') 
    if request.method == "POST": 
        form = TodoForm(request.POST) 
        if form.is_valid(): 
            form.save() 
    form = TodoForm()
    page = { 
             "forms" : form, 
             "list" : item_list, 
             "title" : "TODO LIST", 
             "username" : username
           } 
    return render(request,'diary/intern_calendar_user.html' , page)   


@login_required
def user_placement_calendar(request,username):
    item_list = Todo1.objects.filter(username__username=username).order_by('-date') 
    if request.method == "POST": 
        form = Todo1Form(request.POST) 
        if form.is_valid(): 
            form.save() 
    form = Todo1Form()
    page = { 
             "forms" : form, 
             "list" : item_list, 
             "title" : "TODO LIST", 
             "username" : username
           } 
    return render(request,'diary/placement_calendar_user.html' , page) 

def activities_list(request):
    l=activities.objects.all().order_by('-date')
    return render(request,'diary/activities.html',{'l':l})