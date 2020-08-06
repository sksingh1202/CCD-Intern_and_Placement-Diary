from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Company)
admin.site.register(models.HR)
admin.site.register(models.Remark)
