from django.dispatch import Signal
from django.db.models.signals import post_save,pre_save,pre_delete
from django.contrib.auth.models import User
from django.contrib.auth import user_logged_in,user_logged_out
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry
from .models import Todo,activities,Todo1,Company,HR

new_task= Signal(providing_args=["Todo"])
new_task1=Signal(providing_args=["Todo1"])
intern_task_delete=Signal(providing_args=["Todo"])
intern_task_delete2=Signal(providing_args=["Todo1"])
new_company=Signal(providing_args=["Company"])
new_HR=Signal(providing_args=["HR"])

@receiver(post_save,sender=Todo)
def activity(sender,instance,**kwargs):
    activities.objects.create(username=instance.username,details='has created a task in interns section')

@receiver(post_save,sender=Todo1)
def activity1(sender,instance,**kwargs):
    activities.objects.create(username=instance.username,details='has created a task in placements section')

@receiver(pre_delete,sender=Todo)
def intern_task_delete1(sender,instance,**kwargs):
    activities.objects.create(username=instance.username,details='has deleted a task in intern section')

@receiver(pre_delete,sender=Todo1)
def intern_task_delete3(sender,instance,**kwargs):
    activities.objects.create(username=instance.username,details='has deleted a task in placement section')        


@receiver(post_save,sender=Company)
def new_company2(sender,instance,**kwargs):
    activities.objects.create(username=instance.user,company_name=instance.name,details='has added a company')

@receiver(post_save,sender=HR)
def new_hr(sender,instance,**kwargs):
    activities.objects.create(username=instance.user,company_name=instance.company.name,details='has added a HR for company')        