from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .forms import BasicDatasetForm, PartnerForm, DataReqForm, ExpStepForm, ReportingForm
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting
import json
from django.http import JsonResponse
import datetime
import functions, PDFexport

import pdb

# Django exceptions
from django.core.exceptions import ObjectDoesNotExist



def participate(request):

    try:
        dataset_list = BasicDataset.objects.all()

        context = {
            'dataset_list': dataset_list,
            'show_participate': True,
            'show_review': False,
        }

        return render(request, 'protocoltool/protocoloverview.html', context)

    except ObjectDoesNotExist:
        raise Http404


def review(request):

    try:
        dataset_list = BasicDataset.objects.all()

        context = {
            'dataset_list': dataset_list,
            'show_participate': False,
            'show_review': True,
        }

        return render(request, 'protocoltool/protocoloverview.html', context)

    except ObjectDoesNotExist:
        raise Http404


def protocolOverviewAction(request):

    postDict = request.POST.dict()

    dataset_id = postDict['dataset_id']
    action = postDict['dataset_action']

    dataset_obj = BasicDataset.objects.get(id=dataset_id)

    if action == 'view':
        # go to URL that shows HTML page with all form info
        url = '/view/%s/' % dataset_obj.id
        return HttpResponseRedirect(url)

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
        url = '/form/%s/' % dataset_obj.id
        return HttpResponseRedirect(url)

    return HttpResponseRedirect(reverse('protocoltool:protocoloverview_review'))


def createProtocol(request):

    # Create empty dataset
    core_obj = BasicDataset(
        title='',
        shortname='',
        dateLastUpdate = str(datetime.date.today())
        )

    core_obj.save()

    url = '/form/%s/' % core_obj.id
    return HttpResponseRedirect(url)


def viewProtocol(request, dataset_id):
    '''
    Show all information of the protocol
    :param request:
    :param dataset_id: id of the protocol from the post request
    :return:
    '''

    datasetID = int(dataset_id)
    # context = getAllProtocolInfo(dataset_id)

    context = {}
    context['basic'] = BasicDataset.objects.get(id=datasetID)
    context['partners'] = Partner.objects.filter(dataset_id=datasetID)
    context['methods'] = DataReq.objects.filter(dataset_id=datasetID)
    context['steps'] = ExpStep.objects.filter(dataset_id=datasetID)
    context['results'] = Reporting.objects.filter(dataset_id=datasetID)

    return render(request, 'protocoltool/viewprotocol.html', context)



def formAll(request, dataset_id="0"):

    '''
    Open the form for editing
    :param request:
    :param dataset_id: id of the dataset to show the form
    :return:
    '''

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
            shortname=content['shortname'],
            experimentIdea = content['experimentIdea'],
            hypothesis = content['hypothesis'],
            researchObjective = content['researchObjective'],
            checked = True,
            dateLastUpdate = str(datetime.date.today())
        )
        core_obj.save()

        return HttpResponseRedirect(reverse('protocoltool:protocoloverview_participate'))

    return HttpResponseRedirect(reverse('protocoltool:protocoloverview_participate'))


def getAllProtocolInfo(datasetID):

    '''
    Retrieve all info of a protocol
    :param datasetID: ID of the dataset (protocol) to get all information from
    :return: dictionary with all information of the dataset
    '''

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
        'existingPartnersJSON': json.dumps(existingPartnersList),
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

