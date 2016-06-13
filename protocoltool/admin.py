from django.contrib import admin
from .models import BasicDataset, Project, Partner, LinkProtocol, TemporalExtend

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'leader', 'e_mail')

class BasicDatasetAdmin(admin.ModelAdmin):
    list_display = ('title',
            'experimentIdea',
            'hypothesis',
            'researchObjective',
            'principles',
            'dataReqDescription',
            'dataReqProperties',
            'dataReqContributingPartner',
            'dataReqSubmDate',
            'expExecutionSteps',
            'resultReportingFormatting')

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'lead')

class TemporalExtendAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'start_date', 'end_date')

admin.site.register(BasicDataset, BasicDatasetAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(LinkProtocol)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TemporalExtend, TemporalExtendAdmin)