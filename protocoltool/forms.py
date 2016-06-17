from django import forms
from .models import BasicDataset, Partner, DataReq, ExpStep, ResultRep
from django.forms.widgets import DateInput, NumberInput, Select, Textarea, TextInput, EmailInput

class BasicDatasetForm(forms.ModelForm):
    class Meta:
        model = BasicDataset
        fields = [
            'title',
            'experimentIdea',
            'hypothesis',
            'researchObjective',
            'principles'
        ]
        labels = {
            'title': 'Protocol name',
            'experimentIdea': 'Experiment Idea',
            'hypothesis' : 'Hypothesis',
            'researchObjective': 'Research Objective',
            'principles': 'Principles'
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
            )
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


class DataReqForm(forms.ModelForm):
    class Meta:
        model = DataReq
        fields = [
            'description',
            'properties',
            'deadline'
        ]
        labels = {
            'description': 'Description',
            'properties': 'Properties',
            'deadline': 'Deadline'
        }
        widgets = {
            'description': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'properties': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }

class ExpStepForm(forms.ModelForm):
    class Meta:
        model = ExpStep
        fields = [
            'description',
            'output',
            'deadline'
        ]
        labels = {
            'description': 'Description',
            'output': 'Output',
            'deadline': 'Deadline'
        }
        widgets = {
            'description': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'output': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }

class ResultRepForm(forms.ModelForm):
    class Meta:
        model = ResultRep
        fields = [
            'description',
            'output',
            'deadline'
        ]
        labels = {
            'description': 'Description',
            'output': 'Output',
            'deadline': 'Deadline'
        }
        widgets = {
            'description': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'output': Textarea(
                attrs={'rows':2, 'class': 'form-control input-sm'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }