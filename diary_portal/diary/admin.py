from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Company)
admin.site.register(models.HR)
admin.site.register(models.Remark)
