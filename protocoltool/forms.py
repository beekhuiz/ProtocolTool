from django import forms
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting
from django.forms.widgets import DateInput, Textarea, TextInput, EmailInput

class BasicDatasetForm(forms.ModelForm):
    class Meta:
        model = BasicDataset
        fields = [
            'title',
            'shortname',
            'experimentIdea',
            'hypothesis',
            'researchObjective',
        ]
        labels = {
            'title': 'Full experiment name',
            'shortname': 'Short name',
            'experimentIdea': 'Experiment Idea',
            'hypothesis' : 'Hypothesis',
            'researchObjective': 'Research Objective',
        }
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            ),
            'shortname': TextInput(
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
            'task',
            'description',
            'deadline',
            'done',
        ]
        labels = {
            'task': 'Task',
            'description': 'Description',
            'deadline': 'Deadline',
            'done': 'Done',
        }
        widgets = {
            'task': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm reqtask', 'placeholder': 'Short description of the protocol'}
            ),
            'description': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm reqdesc', 'placeholder': 'e.g. time period, domain, etc.'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm reqdeadline', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }

class ExpStepForm(forms.ModelForm):
    class Meta:
        model = ExpStep
        fields = [
            'task',
            'properties',
            'deadline'
        ]
        labels = {
            'task': 'Task',
            'properties': 'Output',
            'deadline': 'Deadline'
        }
        widgets = {
            'task': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm expsteptask', 'placeholder': 'e.g. transform data, createinput files, run model'}
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
            'task',
            'properties',
            'deadline'
        ]
        labels = {
            'task': 'Task',
            'properties': 'Output',
            'deadline': 'Deadline'
        }
        widgets = {
            'task': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm reportingtask', 'placeholder': 'e.g. findings, '}
            ),
            'properties': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm reportingproperties', 'placeholder': 'e.g. graphs, maps, etc.'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm reportingdeadline', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }