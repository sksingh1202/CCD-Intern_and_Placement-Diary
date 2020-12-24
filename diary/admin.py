from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from .models import Todo,Todo1

# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name_display','year']
    list_filter = ['POC','placement','internship','year']
    list_display = ['name_display','POC','additional_POC','placement','internship']
    list_editable = ['POC','additional_POC']

    def name_display(self, obj):
        return obj.name + " (" + str(obj.year) + ")"

class   HRAdmin(admin.ModelAdmin):
    search_fields = ['company']
    list_filter = ['company']
    list_display =['name','company','contact_number_1','contact_number_2','email','linkedin_id','facebook_id']


class RemarkAdmin(admin.ModelAdmin):
    search_fields = ['company','user']
    list_filter = ['company','user']
    list_display = ['remark_display','company','user','datetime','placement']

    def remark_display(self, obj):
        if len(obj.remark) > 30:
            return obj.remark[:30] + "..."
        return obj.remark

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Company,CompanyAdmin)
admin.site.register(models.HR,HRAdmin)
admin.site.register(models.Remark,RemarkAdmin)
admin.site.register(Todo)
admin.site.register(Todo1)
