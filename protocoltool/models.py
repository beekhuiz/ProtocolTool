from django.db import models
# Create your models here.

class Project(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100)
    number = models.CharField(max_length=11)
    leader = models.CharField(max_length=60)
    e_mail = models.EmailField(max_length=254)


class BasicDataset(models.Model):
    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=200)
    experimentIdea = models.TextField()
    hypothesis = models.TextField()
    researchObjective = models.TextField()
    principles = models.TextField(blank=True)
    dataReqDescription = models.TextField(blank=True)
    dataReqProperties = models.TextField(blank=True)
    dataReqContributingPartner = models.CharField(max_length=200, blank=True)
    dataReqSubmDate = models.DateField(blank=True, null=True)
    expExecutionSteps = models.CharField(max_length=200, blank=True)
    resultReportingFormatting = models.CharField(max_length=200, blank=True)

    published = models.BooleanField(default=False)


class Partner(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    lead = models.BooleanField()
    dataset = models.ForeignKey(BasicDataset)


class TemporalExtend(models.Model):
    def __unicode__(self):
        return self.dataset.title

    dataset = models.ForeignKey(BasicDataset)
    start_date = models.DateField(blank=True, error_messages={'invalid': "Use the format 'yyyy-mm-dd'"})
    end_date = models.DateField(blank=True, error_messages={'invalid': "Use the format 'yyyy-mm-dd'"})


class LinkProtocol(models.Model):
    def __unicode__(self):
        return self.protocol
    protocol = models.CharField(max_length=100)
