from django import forms
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting
from django.forms.widgets import DateInput, Textarea, TextInput, EmailInput

class BasicDatasetForm(forms.ModelForm):
    class Meta:
        model = BasicDataset
        fields = [
            'title',
            'experimentIdea',
            'hypothesis',
            'researchObjective',
        ]
        labels = {
            'title': 'Protocol name',
            'experimentIdea': 'Experiment Idea',
            'hypothesis' : 'Hypothesis',
            'researchObjective': 'Research Objective',
        }
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            ),
            'experimentIdea': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm'}
            ),
            'hypothesis': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm'}
            ),
            'researchObjective': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm'}
            )
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = [
            'name',
            'email',
            'organisation',
            'lead',
        ]

        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            ),
            'email': EmailInput(
                attrs={'class': 'form-control input-sm'}
            ),
            'organisation': TextInput(
                attrs={'class': 'form-control input-sm'}
            ),

        }


class DataReqForm(forms.ModelForm):
    class Meta:
        model = DataReq
        fields = [
            'description',
            'properties',
            'deadline',
            'done',
        ]
        labels = {
            'description': 'Description',
            'properties': 'Properties',
            'deadline': 'Deadline',
            'done': 'Done',
        }
        widgets = {
            'description': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm reqdesc', 'placeholder': 'Short description of the protocol'}
            ),
            'properties': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm reqprop', 'placeholder': 'e.g. time period, domain, etc.'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm reqdeadline', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }

class ExpStepForm(forms.ModelForm):
    class Meta:
        model = ExpStep
        fields = [
            'description',
            'properties',
            'deadline'
        ]
        labels = {
            'description': 'Description',
            'properties': 'Output',
            'deadline': 'Deadline'
        }
        widgets = {
            'description': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm expstepdesc', 'placeholder': 'e.g. transform data, createinput files, run model'}
            ),
            'properties': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm expstepproperties', 'placeholder': 'e.g. variables, formats, etc.'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm expstepdeadline', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }

class ReportingForm(forms.ModelForm):
    class Meta:
        model = Reporting
        fields = [
            'description',
            'properties',
            'deadline'
        ]
        labels = {
            'description': 'Description',
            'properties': 'Output',
            'deadline': 'Deadline'
        }
        widgets = {
            'description': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm reportingdesc', 'placeholder': 'e.g. findings, '}
            ),
            'properties': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm reportingproperties', 'placeholder': 'e.g. graphs, maps, etc.'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm reportingdeadline', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }