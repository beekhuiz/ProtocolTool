import os
# Imports for responding
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
# Imports of models
from .forms import BasicDatasetForm, PartnerForm, DataReqForm, ExpStepForm, ReportingForm
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting
import json
# from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.utils.safestring import mark_safe
from django.http import JsonResponse
import datetime
import functions, PDFexport

import pdb

# Django exceptions
from django.core.exceptions import ObjectDoesNotExist


def detail(request):

    context = {}

    if request.method == 'POST':
        postDict = request.POST.dict()

        dataset_id = postDict['dataset_id']
        action = postDict['dataset_action']

        dataset_obj = BasicDataset.objects.get(id=dataset_id)

        if action == 'delete':
            # Remove metadata in database
            BasicDataset.objects.filter(id=dataset_id).delete()

        elif action == 'publish':
            # Fill in dataset published field
            dataset_obj.published = True
            dataset_obj.save()

        elif action == 'unpublish':
            # Empty the dataset published field
            if dataset_obj.published is not None:
                dataset_obj.published = False
                dataset_obj.save()

        elif action == 'export':
            response = PDFexport.createPDF(dataset_id)
            return response

        elif action == 'edit':
            # Get core model data
            # core_data = BasicDataset.objects.get(id=dataset_id)
            # return HttpResponseRedirect(reverse('protocoltool:edit_dataset', kwargs={'dataset_id': dataset_id}))
            url = '/form/%s/' % dataset_obj.id
            return HttpResponseRedirect(url)

        return HttpResponseRedirect(reverse('protocoltool:detail'))

    elif request.method == 'GET':
        try:
            dataset_list = BasicDataset.objects.all()
            context.update({
                'dataset_list': dataset_list,
            })
        except ObjectDoesNotExist:
            raise Http404

    return render(request, 'protocoltool/detail.html', context)


def formBasic(request):

    # Create empty dataset
    core_obj = BasicDataset(
        title='',
        dateLastUpdate = str(datetime.date.today())
        )

    core_obj.save()

    url = '/form/%s/' % core_obj.id
    return HttpResponseRedirect(url)


def formAll(request, dataset_id="0"):

    #pdb.set_trace()

    dataset_id = int(dataset_id)

    if request.method == 'GET' and dataset_id != 0:
        context = getAllProtocolInfo(dataset_id)
        return render(request, 'protocoltool/form.html', context)


    elif request.method == 'POST' and dataset_id != 0:
        content = request.POST

        # update the basic information of the protocol
        core_obj = BasicDataset(
            id=dataset_id,
            title=content['title'],
            experimentIdea = content['experimentIdea'],
            hypothesis = content['hypothesis'],
            researchObjective = content['researchObjective'],
            checked = True,
            dateLastUpdate = str(datetime.date.today())
        )
        core_obj.save()

        return HttpResponseRedirect(
            reverse('protocoltool:detail'))

    return HttpResponseRedirect(reverse('protocoltool:detail'))


def getAllProtocolInfo(datasetID):

    coreData = BasicDataset.objects.get(id=datasetID)
    formCore = BasicDatasetForm(instance=coreData, auto_id='id_basic_%s')

    # Load in existing partners
    existingPartnersList = functions.getPartnersList(datasetID)

    formPartner = PartnerForm()

    # Load in data
    existingReqsList = functions.getReqsList(datasetID)
    existingExpStepsList = functions.getExpStepsList(datasetID)
    existingReportingsList = functions.getReportingsList(datasetID)

    formDataReq = DataReqForm()
    formExpStep = ExpStepForm()
    formReporting = ReportingForm()

    formList = [
        ['Basic', formCore],
        ['Partner', formPartner],
        ['DataReq', formDataReq],
        ['ExpStep', formExpStep],
        ['Reporting', formReporting],
    ]

    context = {}

    context.update({
        'edit': True,
        'dataset_id': datasetID,
        'existingPartnersJSON': json.dumps(existingPartnersList), #mark_safe(existingPartnersJSON),#json.dumps(list(existingPartners), cls=DjangoJSONEncoder),
        'existingReqsJSON': json.dumps(existingReqsList),
        'existingExpStepsJSON': json.dumps(existingExpStepsList),
        'existingReportingsJSON': json.dumps(existingReportingsList),
        'forms_list': formList
    })

    return context



"""
PARTNERS
"""

def addPartner(request):

    postDict = request.POST.dict()

    # update the Partner model based on the post information from the client
    functions.createPartnerModelFromClient(postDict, False)

    # send back the new Partner model as a list to use client side
    existingPartnersList = functions.getPartnersList(postDict['datasetID'])
    return JsonResponse({'existingPartnersJSON': json.dumps(existingPartnersList)})


def updatePartner(request):

    postDict = request.POST.dict()

    # update the Partner model based on the post information from the client
    functions.createPartnerModelFromClient(postDict, True)

    # send back the new Partner model as a list to use client side
    existingPartnersList = functions.getPartnersList(postDict['datasetID'])
    return JsonResponse({'existingPartnersJSON': json.dumps(existingPartnersList)})


def deletePartner(request):

    postDict = request.POST.dict()

    Partner.objects.filter(id=postDict['partnerID']).delete()

    # send back the new Request model as a list to use client side
    existingPartnersList = functions.getPartnersList(postDict['datasetID'])
    return JsonResponse({'existingPartnersJSON': json.dumps(existingPartnersList)})


"""
DATA PREPARATION
"""

def addReq(request):

    postDict = request.POST.dict()

    # add a new Request model based on the post information from the client
    functions.createReqModelFromClient(postDict, False)

    # send back the new Request model as a list to use client side
    existingReqsList = functions.getReqsList(postDict['datasetID'])
    return JsonResponse({'existingReqsJSON': json.dumps(existingReqsList)})


def updateReq(request):
    postDict = request.POST.dict()

    # update the Request model based on the post information from the client
    functions.createReqModelFromClient(postDict, True)

    # send back the new Request model as a list to use client side
    existingReqsList = functions.getReqsList(postDict['datasetID'])
    return JsonResponse({'existingReqsJSON': json.dumps(existingReqsList)})


def deleteReq(request):

    postDict = request.POST.dict()

    DataReq.objects.filter(id=postDict['reqID']).delete()

    # send back the new Request model as a list to use client side
    existingReqsList = functions.getReqsList(postDict['datasetID'])
    return JsonResponse({'existingReqsJSON': json.dumps(existingReqsList)})


"""
EXPERIMENT STEPS
"""

def addExpStep(request):

    postDict = request.POST.dict()

    # add a new ExpStep model based on the post information from the client
    functions.createExpStepModelFromClient(postDict, False)

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getExpStepsList(postDict['datasetID'])
    return JsonResponse({'existingExpStepsJSON': json.dumps(existingExpStepsList)})


def updateExpStep(request):
    postDict = request.POST.dict()

    # update the ExpStep model based on the post information from the client
    functions.createExpStepModelFromClient(postDict, True)

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getExpStepsList(postDict['datasetID'])
    return JsonResponse({'existingExpStepsJSON': json.dumps(existingExpStepsList)})


def deleteExpStep(request):

    postDict = request.POST.dict()

    ExpStep.objects.filter(id=postDict['expStepID']).delete()

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getExpStepsList(postDict['datasetID'])
    return JsonResponse({'existingExpStepsJSON': json.dumps(existingExpStepsList)})



"""
REPORTING STEPS
"""

def addReporting(request):

    postDict = request.POST.dict()

    # add a new Reporting model based on the post information from the client
    functions.createReportingModelFromClient(postDict, False)

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getReportingsList(postDict['datasetID'])
    return JsonResponse({'existingReportingsJSON': json.dumps(existingReportingsList)})


def updateReporting(request):
    postDict = request.POST.dict()

    # update the Reporting model based on the post information from the client
    functions.createReportingModelFromClient(postDict, True)

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getReportingsList(postDict['datasetID'])
    return JsonResponse({'existingReportingsJSON': json.dumps(existingReportingsList)})


def deleteReporting(request):

    postDict = request.POST.dict()

    Reporting.objects.filter(id=postDict['reportingID']).delete()

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getReportingsList(postDict['datasetID'])
    return JsonResponse({'existingReportingsJSON': json.dumps(existingReportingsList)})

