from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .forms import BasicDatasetForm, PartnerForm, DataReqForm, ExpStepForm, ReportingForm
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting, ExternalProtocol
from django.forms.models import model_to_dict
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
        externalProtocol_list = ExternalProtocol.objects.all()

        context = {
            'dataset_list': dataset_list,
            'external_protocol_list': externalProtocol_list,
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
        dateLastUpdate=str(datetime.date.today())
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
    context['methods'] = DataReq.objects.filter(dataset_id=datasetID).order_by('taskNr')
    context['steps'] = ExpStep.objects.filter(dataset_id=datasetID).order_by('taskNr')
    context['results'] = Reporting.objects.filter(dataset_id=datasetID).order_by('taskNr')

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
        # content = request.POST

        # title = content['title']
        # shortname = content['shortname']

        # update the basic information of the protocol
        # core_obj = BasicDataset(
        #     # id=dataset_id,
        #     # title=content['title'],
        #     # shortname=content['shortname'],
        #     # experimentIdea=content['experimentIdea'],
        #     # hypothesis=content['hypothesis'],
        #     # researchObjective=content['researchObjective'],
        #     # checked=True,
        #     dateLastUpdate=str(datetime.date.today())
        # )
        # core_obj.save()

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

    # Load in data
    existingExperimentInfoDict = functions.getExperimentInfoDict(datasetID)
    existingPartnersList = functions.getPartnersList(datasetID)
    existingReqsList = functions.getListSteps(datasetID, DataReq)
    existingExpStepsList = functions.getListSteps(datasetID, ExpStep)
    existingReportingsList = functions.getListSteps(datasetID, Reporting)

    formPartner = PartnerForm(auto_id='id_partner_%s')
    formDataReq = DataReqForm(auto_id='id_req_%s')
    formExpStep = ExpStepForm(auto_id='id_exp_%s')
    formReporting = ReportingForm(auto_id='id_reporting_%s')

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
        'existingExperimentInfoJSON': json.dumps(existingExperimentInfoDict),
        'existingPartnersJSON': json.dumps(existingPartnersList),
        'existingReqsJSON': json.dumps(existingReqsList),
        'existingExpStepsJSON': json.dumps(existingExpStepsList),
        'existingReportingsJSON': json.dumps(existingReportingsList),
        'forms_list': formList
    })

    return context


def saveExperimentInfo(request):

    postDict = request.POST.dict()

    # create new partner object
    BasicDataset.objects.filter(id=postDict['datasetID']).update(
        title=postDict['title'],
        shortname=postDict['shortname'],
        experimentIdea=postDict['experimentIdea'],
        hypothesis=postDict['hypothesis'],
        researchObjective=postDict['researchObjective'],
        checked=True,
        dateLastUpdate=str(datetime.date.today()))

    # convert the basic dataset (=experiment info) to a dictionary
    existingExperimentInfoDict = functions.getExperimentInfoDict(postDict['datasetID'])
    return JsonResponse({'existingExperimentInfoJSON': json.dumps(existingExperimentInfoDict)})


# region PARTNERS
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


# endregion


# region DATA PREPARATION
"""
DATA PREPARATION
"""


def addReq(request):
    postDict = request.POST.dict()

    # add a new Request model based on the post information from the client
    functions.createStepModelFromClient(postDict, False, DataReq)

    # send back the new Request model as a list to use client side
    existingReqsList = functions.getListSteps(postDict['datasetID'], DataReq)
    return JsonResponse({'existingListJSON': json.dumps(existingReqsList)})


def updateReq(request):
    postDict = request.POST.dict()

    # update the Request model based on the post information from the client
    functions.createStepModelFromClient(postDict, True, DataReq)

    # send back the new Request model as a list to use client side
    existingReqsList = functions.getListSteps(postDict['datasetID'], DataReq)
    return JsonResponse({'existingListJSON': json.dumps(existingReqsList)})


def deleteReq(request):
    postDict = request.POST.dict()

    functions.updateTaskNrs(postDict['datasetID'], postDict['stepID'], DataReq)

    DataReq.objects.filter(id=postDict['stepID']).delete()

    # send back the new Request model as a list to use client side
    existingReqsList = functions.getListSteps(postDict['datasetID'], DataReq)
    return JsonResponse({'existingListJSON': json.dumps(existingReqsList)})


def increaseReq(request):
    postDict = request.POST.dict()
    functions.increaseTaskNr(postDict['datasetID'], postDict['reqID'], DataReq)

    # send back the new Reqs model as a list to use client side
    existingReqsList = functions.getListSteps(postDict['datasetID'], DataReq)
    return JsonResponse({'existingListJSON': json.dumps(existingReqsList)})


def decreaseReq(request):
    postDict = request.POST.dict()
    functions.decreaseTaskNr(postDict['datasetID'], postDict['reqID'], DataReq)

    # send back the new Reqs model as a list to use client side
    existingReqsList = functions.getListSteps(postDict['datasetID'], DataReq)
    return JsonResponse({'existingListJSON': json.dumps(existingReqsList)})


# endregion


# region EXPERIMENT STEPS
"""
EXPERIMENT STEPS
"""


def addExpStep(request):
    postDict = request.POST.dict()

    # add a new ExpStep model based on the post information from the client
    functions.createStepModelFromClient(postDict, False, ExpStep)

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getListSteps(postDict['datasetID'], ExpStep)
    return JsonResponse({'existingListJSON': json.dumps(existingExpStepsList)})


def updateExpStep(request):
    postDict = request.POST.dict()

    # update the ExpStep model based on the post information from the client
    functions.createStepModelFromClient(postDict, True, ExpStep)

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getListSteps(postDict['datasetID'], ExpStep)
    return JsonResponse({'existingListJSON': json.dumps(existingExpStepsList)})


def deleteExpStep(request):
    postDict = request.POST.dict()

    functions.updateTaskNrs(postDict['datasetID'], postDict['stepID'], ExpStep)

    ExpStep.objects.filter(id=postDict['stepID']).delete()

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getListSteps(postDict['datasetID'], ExpStep)
    return JsonResponse({'existingListJSON': json.dumps(existingExpStepsList)})


def increaseExpStep(request):
    postDict = request.POST.dict()
    functions.increaseTaskNr(postDict['datasetID'], postDict['expStepID'], ExpStep)

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getListSteps(postDict['datasetID'], ExpStep)
    return JsonResponse({'existingListJSON': json.dumps(existingExpStepsList)})


def decreaseExpStep(request):
    postDict = request.POST.dict()
    functions.decreaseTaskNr(postDict['datasetID'], postDict['expStepID'], ExpStep)

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getListSteps(postDict['datasetID'], ExpStep)
    return JsonResponse({'existingListJSON': json.dumps(existingExpStepsList)})


# endregion


#region REPORTING STEPS
"""
REPORTING STEPS
"""


def addReporting(request):
    postDict = request.POST.dict()

    # add a new Reporting model based on the post information from the client
    functions.createStepModelFromClient(postDict, False, Reporting)

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getListSteps(postDict['datasetID'], Reporting)
    return JsonResponse({'existingListJSON': json.dumps(existingReportingsList)})


def updateReporting(request):
    postDict = request.POST.dict()

    # update the Reporting model based on the post information from the client
    functions.createStepModelFromClient(postDict, True, Reporting)

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getListSteps(postDict['datasetID'], Reporting)
    return JsonResponse({'existingListJSON': json.dumps(existingReportingsList)})


def deleteReporting(request):
    postDict = request.POST.dict()

    functions.updateTaskNrs(postDict['datasetID'], postDict['stepID'], Reporting)
    Reporting.objects.filter(id=postDict['stepID']).delete()

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getListSteps(postDict['datasetID'], Reporting)
    return JsonResponse({'existingListJSON': json.dumps(existingReportingsList)})


def increaseReporting(request):
    postDict = request.POST.dict()
    functions.increaseTaskNr(postDict['datasetID'], postDict['reportingID'], Reporting)

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getListSteps(postDict['datasetID'], Reporting)
    return JsonResponse({'existingListJSON': json.dumps(existingReportingsList)})


def decreaseReporting(request):
    postDict = request.POST.dict()
    functions.decreaseTaskNr(postDict['datasetID'], postDict['reportingID'], Reporting)

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getListSteps(postDict['datasetID'], Reporting)
    return JsonResponse({'existingListJSON': json.dumps(existingReportingsList)})

# endregion
