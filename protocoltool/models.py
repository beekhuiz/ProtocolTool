from django.db import models
import datetime

from django.contrib.auth.models import User

class BasicDataset(models.Model):
    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=200)
    shortname = models.CharField(max_length=100)
    experimentIdea = models.TextField(blank=True)
    hypothesis = models.TextField(blank=True)
    researchObjective = models.TextField(blank=True)

    dateLastUpdate = models.DateField(blank=True, default=datetime.date.today)
    checked = models.BooleanField(default=False)
    published = models.BooleanField(default=False)


class Partner(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    organisation = models.CharField(max_length=100)
    lead = models.BooleanField(default=False)
    dataset = models.ForeignKey(BasicDataset)


class DataReq(models.Model):
    task = models.TextField(blank=True)
    description = models.TextField(blank=True)
    partner = models.ForeignKey(Partner)
    deadline = models.DateField(blank=True, default=datetime.date.today)
    done = models.BooleanField(default=False)
    dataset = models.ForeignKey(BasicDataset)


class ExpStep(models.Model):
    task = models.TextField(blank=True)
    properties = models.TextField(blank=True)
    partner = models.ForeignKey(Partner)
    deadline = models.DateField(blank=True, default=datetime.date.today)
    dataset = models.ForeignKey(BasicDataset)


class Reporting(models.Model):
    task = models.TextField(blank=True)
    taskNr = models.IntegerField(default=1)
    properties = models.TextField(blank=True)
    partner = models.ForeignKey(Partner)
    deadline = models.DateField(blank=True, default=datetime.date.today)
    dataset = models.ForeignKey(BasicDataset)


class ExternalProtocol(models.Model):
    shortname = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    dateLastUpdate = models.DateField(blank=True, default=datetime.date.today)