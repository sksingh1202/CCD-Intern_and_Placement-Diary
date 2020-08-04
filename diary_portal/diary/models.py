from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from diary_portal import settings

# this is from an external package:django-phonenumber-field
# see: https://github.com/stefanfoulis/django-phonenumber-field
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

# this is for making a custom user model which adds in additional features from the built in
# see https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#auth-custom-user
class User(AbstractUser):
    def __str__(self):
        return self.username

class Company(models.Model):
    name = models.CharField(max_length=100)
    POC = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='company_poc')
    CPOC = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='company_cpoc')
    additional_POC = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    placement = models.BooleanField()

    def __str__(self):
        return self.name

class Remark(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='remarks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='remarks')
    remark = models.TextField()
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.remark[:20] + "..."

class HR(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='hr')
    contact_number_1 = PhoneNumberField(blank = True)
    contact_number_2 = PhoneNumberField(blank = True)
    email = models.EmailField(blank = True)
    linkedin_id = models.CharField(max_length=50, blank=True)
    facebook_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
