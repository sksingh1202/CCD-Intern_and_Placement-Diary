from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
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
    name = models.CharField(max_length=100, unique=True)
    POC = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='company_poc')
    CPOC = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='company_cpoc')
    additional_POC = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(blank=True)
    placement = models.BooleanField(default=False)
    internship = models.BooleanField(default=False)
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company_list')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

class Remark(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='remarks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='remarks')
    remark = models.TextField()
    datetime = models.DateTimeField(auto_now=True)
    placement = models.BooleanField(default=False)

    def __str__(self):
        return self.remark[:20] + "..."

    class Meta:
        ordering = ['datetime']
        verbose_name = "Remark"
        verbose_name_plural = "Remarks"

class HR(models.Model):
    name = models.CharField(max_length=100)
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

    class Meta:
        verbose_name = "HR"
        verbose_name_plural = "HRs"
