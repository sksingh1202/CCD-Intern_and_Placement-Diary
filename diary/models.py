from django.db import models
from django.db.models.functions import ExtractYear
from django.contrib.auth.models import AbstractUser
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.utils import timezone
from diary_portal import settings

import datetime as python_datetime
import os

# this is from an external package:django-phonenumber-field
# see: https://github.com/stefanfoulis/django-phonenumber-field
from phonenumber_field.modelfields import PhoneNumberField

#api related code
import clearbit
clearbit.key = os.environ.get('CLEARBIT_KEY')
# Create your models here.

# this is for making a custom user model which adds in additional features from the built in
# see https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#auth-custom-user
class User(AbstractUser):
    def __str__(self):
        return self.username

class Company(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='companies')
    POC = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='company_poc')
    CPOC = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='company_cpoc')
    additional_POC = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    placement = models.BooleanField(default=False)
    internship = models.BooleanField(default=False)
    slug = models.SlugField(editable=False, allow_unicode=True, blank=True)
    # you need to add auto_now_add = True and remove default during deployment
    datetime = models.DateTimeField(default=timezone.now)
    # you need to do editable = False and remove default during deployment
    year = models.IntegerField(blank=True, default=python_datetime.date.today().year)
    info = models.JSONField(blank=True, editable=False, null=True)

    def __str__(self):
        return self.name + " (" + str(self.year) + ")"

    def get_absolute_url(self):
        return reverse('company_list', kwargs={'year':python_datetime.date.today().year})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        dom = clearbit.NameToDomain.find(name=self.name)
        if dom is not None:
            self.info = clearbit.Company.find(domain=dom['domain'])
        # uncomment during deployment
        # self.year = python_datetime.date.today().year
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['name', 'year']
        ordering = ['-datetime']
        verbose_name = "Company"
        verbose_name_plural = "Companies"

class Remark(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='remarks', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='remarks', blank=True)
    remark = models.TextField()
    # do auto_now_add=True and remove default during deployment
    datetime = models.DateTimeField(default=timezone.now)
    placement = models.BooleanField(default=False, blank = True)

    def __str__(self):
        return self.remark[:30] + "..."

    class Meta:
        ordering = ['datetime']
        verbose_name = "Remark"
        verbose_name_plural = "Remarks"

class HR(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='hr')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='hr')
    contact_number_1 = PhoneNumberField(blank = True)
    contact_number_2 = PhoneNumberField(blank = True)
    email = models.EmailField(blank = True)
    linkedin_id = models.CharField(max_length=50, blank=True)
    facebook_id = models.CharField(max_length=50, blank=True)
    placement = models.BooleanField(default=False)
    internship = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.placement:
            return reverse_lazy('company_placement_remarks_list', kwargs={'slug':self.company.slug, 'year':self.company.year})
        else:
            return reverse_lazy('company_intern_remarks', kwargs={'slug':self.company.slug, 'year':self.company.year})

    class Meta:
        verbose_name = "HR"
        verbose_name_plural = "HRs"

class Todo(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='tasks', blank=True)
    title=models.CharField(max_length=100) 
    details=models.TextField() 
    date=models.DateTimeField(default=timezone.now) 
  
    def __str__(self): 
        return self.title

class Todo1(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='tasks1', blank=True)
    title=models.CharField(max_length=100) 
    details=models.TextField() 
    date=models.DateTimeField(default=timezone.now) 
  
    def __str__(self): 
        return self.title

class activities(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='activities', blank=True)
    details=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    company_name=models.TextField(default='')
    # date=models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.username

