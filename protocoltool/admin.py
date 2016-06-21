from django.contrib import admin
from .models import BasicDataset, Partner, DataReq, ExpStep, ResultRep

# Register your models here.

class BasicDatasetAdmin(admin.ModelAdmin):
    list_display = ('title',
            'experimentIdea',
            'hypothesis',
            'researchObjective',
            'principles',
            'published',
            'checked')

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'lead')

class DataReqAdmin(admin.ModelAdmin):
    list_display = ('description', 'properties', 'partner', 'deadline')

class ExpStepAdmin(admin.ModelAdmin):
    list_display = ('description', 'output', 'partner', 'deadline')

class ResultRepAdmin(admin.ModelAdmin):
    list_display = ('description', 'output', 'partner', 'deadline')

admin.site.register(BasicDataset, BasicDatasetAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(DataReq, DataReqAdmin)
admin.site.register(ExpStep, ExpStepAdmin)
admin.site.register(ResultRep, ResultRepAdmin)
