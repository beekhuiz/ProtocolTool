from django import forms
from .models import BasicDataset, Partner, TemporalExtend
from django.forms.widgets import DateInput, NumberInput, Select, Textarea, TextInput, EmailInput

class BasicDatasetForm(forms.ModelForm):
    class Meta:
        model = BasicDataset
        fields = [
            'title',
            'experimentIdea',
            'hypothesis',
            'researchObjective',
            'principles',
            'dataReqDescription',
            'dataReqProperties',
            'dataReqContributingPartner',
            'dataReqSubmDate',
            'expExecutionSteps',
            'resultReportingFormatting'
        ]
        labels = {
            'title': 'Protocol name',
            'experimentIdea': 'Experiment Idea',
            'hypothesis' : 'Hypothesis',
            'researchObjective': 'Research Objective',
            'principles': 'Principles',
            'dataReqDescription': 'Description',
            'dataReqProperties': 'Data Properties',
            'dataReqContributingPartner': 'Contributing partner',
            'dataReqSubmDate': 'Data submission date',
            'expExecutionSteps': 'Experiment execution steps',
            'resultReportingFormatting': 'Reporting and formatting'
        }
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            ),
            'experimentIdea': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'hypothesis': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'researchObjective': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'principles': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'dataReqDescription': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'dataReqProperties': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'dataReqContributingPartner': TextInput(
                attrs={'class': 'form-control input-sm'}
            ),
            'dataReqSubmDate': DateInput(
                attrs={'class': 'form-control input-sm', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
            'expExecutionSteps': TextInput(
                attrs={'class': 'form-control input-sm'}
            ),
            'resultReportingFormatting': TextInput(
                attrs={'class': 'form-control input-sm'}
            ),
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = [
            'name',
            'email',
            'lead',
        ]

        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            ),
            'email': EmailInput(
                attrs={'class': 'form-control input-sm'}
            ),
        }


class TemporalExtentForm(forms.ModelForm):
    class Meta:
        model = TemporalExtend
        fields = [
            'start_date',
            'end_date',
        ]
        widgets = {
            'start_date': DateInput(
                attrs={'class': 'form-control input-sm', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
            'end_date': DateInput(
                attrs={'class': 'form-control input-sm', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
        }
        error_messages = {
            'start_date': {
                'invalid': 'Use the format: yyyy-mm-dd'
            },
            'end_date': {
                'invalid': 'Use the format: yyyy-mm-dd'
            }
        }
