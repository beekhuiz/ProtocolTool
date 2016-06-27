from django.contrib import admin
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting

# Register your models here.

class BasicDatasetAdmin(admin.ModelAdmin):
    list_display = ('title',
            'experimentIdea',
            'hypothesis',
            'researchObjective',
            'published',
            'checked')

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'organisation', 'lead')

class DataReqAdmin(admin.ModelAdmin):
    list_display = ('description', 'properties', 'partner', 'deadline', 'done')

class ExpStepAdmin(admin.ModelAdmin):
    list_display = ('description', 'properties', 'partner', 'deadline')

class ReportingAdmin(admin.ModelAdmin):
    list_display = ('description', 'properties', 'partner', 'deadline')

admin.site.register(BasicDataset, BasicDatasetAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(DataReq, DataReqAdmin)
admin.site.register(ExpStep, ExpStepAdmin)
admin.site.register(Reporting, ReportingAdmin)
