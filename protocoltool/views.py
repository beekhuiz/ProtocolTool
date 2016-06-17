import os
# Imports for responding
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
# Imports of models
from .forms import BasicDatasetForm, PartnerForm, DataReqForm, ExpStepForm, ResultRepForm
from .models import BasicDataset, Partner, DataReq, ExpStep, ResultRep
import json
# from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.utils.safestring import mark_safe
from django.http import JsonResponse
import datetime

import pdb

# Django exceptions
from django.core.exceptions import ObjectDoesNotExist


def detail(request):

    context = {}

    if request.method == 'POST':
        postDict = request.POST

        dataset_id = int(postDict['dataset_id'])
        dataset_obj = BasicDataset.objects.get(id=dataset_id)

        if postDict['dataset_action'] == 'delete':
            # Remove metadata in database
            BasicDataset.objects.filter(id=dataset_id).delete()

        elif postDict['dataset_action'] == 'publish':
            # Fill in dataset published field
            if dataset_obj.published is None:
                dataset_obj.published = datetime.now()
                dataset_obj.save()

        elif postDict['dataset_action'] == 'unpublish':
            # Empty the dataset published field
            if dataset_obj.published is not None:
                dataset_obj.published = None
                dataset_obj.save()

        elif postDict['dataset_action'] == 'edit':
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

    if request.method == 'POST':
        content = request.POST

        if 'form_action' in content:

            # Save Core form
            core_obj = BasicDataset(
                title=content['title'],
                experimentIdea = content['experimentIdea'],
                hypothesis = content['hypothesis'],
                researchObjective = content['researchObjective'],
                principles = content['principles'],
                dateLastUpdate = str(datetime.date.today())
                )

            core_obj.save()

            url = '/form/%s/' % core_obj.id
            return HttpResponseRedirect(url)

        else:
            # User is redirected to main page
            return HttpResponseRedirect(reverse('protocoltool:detail'))

    elif request.method == 'GET':

        formCore = BasicDatasetForm()

        formList = [
            ['Basic', formCore],
        ]

        context = {
            'forms_list': formList
        }

        return render(request, 'protocoltool/formbasic.html', context)


def formAll(request, dataset_id="0"):

    #pdb.set_trace()

    dataset_id = int(dataset_id)
    context = {
    }

    if request.method == 'GET' and dataset_id != 0:
        coreData = BasicDataset.objects.get(id=dataset_id)
        formCore = BasicDatasetForm(instance=coreData, auto_id='id_basic_%s')


        # Load in existing partners
        existingPartners = Partner.objects.filter(dataset__id=dataset_id)

        existingPartnersList = []
        for partner in existingPartners:
            partnerDict = {
                "id": partner.id,
                "name": partner.name,
                "email": partner.email,
                "lead": str(partner.lead),
            }
            existingPartnersList.append(partnerDict)

        formPartner = PartnerForm()


        # Load in existing reqs
        existingReqs = DataReq.objects.filter(dataset__id=dataset_id)

        existingReqsList = []
        for req in existingReqs:
            reqDict = {
                "id": req.id,
                "description": req.description,
                "properties": req.properties,
                "partner": req.partner,
                "deadline": req.deadline,
            }
            existingReqsList.append(reqDict)


        formDataReq = DataReqForm()
        formExpStep = ExpStepForm()

        formList = [
            ['Basic', formCore],
            ['Partner', formPartner],
            ['DataReq', formDataReq],
            ['ExpStep', formExpStep],
        ]

        context.update({
            'edit': True,
            'dataset_id': dataset_id,
            'existingPartners': existingPartners,   # for filling in the initial list; TODO: make this unnecessary: fill in list with jscript
            'existingPartnersJSON': json.dumps(existingPartnersList), #mark_safe(existingPartnersJSON),#json.dumps(list(existingPartners), cls=DjangoJSONEncoder),
            'existingReqs': existingReqs,
            'existingReqsJSON': json.dumps(existingReqsList),
            'forms_list': formList
        })

        return render(request, 'protocoltool/form.html', context)


    elif request.method == 'POST' and dataset_id != 0:
        content = request.POST

        core_obj = BasicDataset(
            id=dataset_id,
            title=content['title'],
            experimentIdea = content['experimentIdea'],
            hypothesis = content['hypothesis'],
            researchObjective = content['researchObjective'],
            principles = content['principles'],
            dateLastUpdate = str(datetime.date.today())
        )
        core_obj.save()

        return HttpResponseRedirect(
            reverse('protocoltool:detail'))

    return HttpResponseRedirect(reverse('protocoltool:detail'))


def addPartner(request):

    newPartner = request.POST.dict()

    # get the foreign key of the protocol dataset of this partner
    dataset = BasicDataset.objects.get(id=newPartner['datasetID'])

    # store the lead as a boolean
    lead = True
    if newPartner['lead'] == 'False':
        lead = False

    # create new partner object
    partnerObj = Partner(
        dataset = dataset,
        name=newPartner['name'],
        email=newPartner['email'],
        lead=lead
        )

    partnerObj.save()

    # reload all partner information as a array list
    existingPartners = Partner.objects.filter(dataset__id=newPartner['datasetID'])

    existingPartnersList = []
    for partner in existingPartners:
        partnerDict = {
            "id": partner.id,
            "name": partner.name,
            "email": partner.email,
            "lead": str(partner.lead),
        }
        existingPartnersList.append(partnerDict)

    #pdb.set_trace()

    # Send all partner information back
    return JsonResponse({'existingPartnersJSON': json.dumps(existingPartnersList)})



def updatePartner(request):

    updatedPartner = request.POST.dict()

    # store the lead as a boolean
    lead = True
    if updatedPartner['lead'] == 'False':
        lead = False

    Partner.objects.filter(id=updatedPartner['partnerID']).update(
        name=updatedPartner['name'],
        email=updatedPartner['email'],
        lead=lead
    )

    # reload all partner information as a array list
    existingPartners = Partner.objects.filter(dataset__id=updatedPartner['datasetID'])

    existingPartnersList = []
    for partner in existingPartners:
        partnerDict = {
            "id": partner.id,
            "name": partner.name,
            "email": partner.email,
            "lead": str(partner.lead),
        }
        existingPartnersList.append(partnerDict)

    # Send all partner information back
    return JsonResponse({'existingPartnersJSON': json.dumps(existingPartnersList)})


def deletePartner(request):

    deletedPartner = request.POST.dict()

    #pdb.set_trace()

    # get the ID of the protocol of this partner
    # dataset = BasicDataset.objects.get(id=updatedPartner['datasetID'])

    Partner.objects.filter(id=deletedPartner['partnerID']).delete()

    # reload all partner information as a array list
    existingPartners = Partner.objects.filter(dataset__id=deletedPartner['datasetID'])

    existingPartnersList = []
    for partner in existingPartners:
        partnerDict = {
            "id": partner.id,
            "name": partner.name,
            "email": partner.email,
            "lead": str(partner.lead),
        }
        existingPartnersList.append(partnerDict)

    # Send all partner information back
    return JsonResponse({'existingPartnersJSON': json.dumps(existingPartnersList)})



def addReq(request):

    postDict = request.POST.dict()
    #pdb.set_trace()


    # get the ID of the protocol of this DataRequest
    dataset = BasicDataset.objects.get(id=postDict['datasetID'])

    # create new partner object
    reqObj = DataReq(
        dataset = dataset,
        description=postDict['description'],
        properties=postDict['properties'],
        partner=postDict['partner'],
        deadline=postDict['deadline']
        )

    reqObj.save()

    # reload all partner information as a array list
    existingReqs = DataReq.objects.filter(dataset__id=postDict['datasetID'])

    existingReqsList = []
    for req in existingReqs:
        reqDict = {
            "id": req.id,
            "description": req.description,
            "properties": req.properties,
            "partner": req.partner,
            "deadline": req.deadline,
        }
        existingReqsList.append(reqDict)

    # Send all partner information back
    return JsonResponse({'existingPartnersJSON': json.dumps(existingReqsList)})




# def form_dataset(request):
#
#     context = {}
#
#     if request.method == 'POST':
#         content = request.POST
#
#         if 'form_action' in content:
#             # A (filled in) form is submitted
#             valid_models = True
#             # Collect basic form data and validate it
#             # formCore = BasicDatasetForm(content, auto_id='id_basic_%s')
#             #
#             # formPartner = PartnerForm(content, auto_id='id_partner_%s')
#             #
#             # formList = [
#             #     ['Basic', formCore],
#             #     ['Partner', formPartner],
#             # ]
#
#             # if not formCore.is_valid() or not form_time.is_valid():
#             #     valid_models = False
#
#
#             # Save Core form
#             core_obj = BasicDataset(
#                 title=content['title'],
#                 experimentIdea = content['experimentIdea'],
#                 hypothesis = content['hypothesis'],
#                 researchObjective = content['researchObjective'],
#                 principles = content['principles'],
#                 dataReqDescription = content['dataReqDescription'],
#                 dataReqProperties = content['dataReqProperties'],
#                 dataReqContributingPartner = content['dataReqContributingPartner'],
#                 dataReqSubmDate = content['dataReqSubmDate'],
#                 expExecutionSteps = content['expExecutionSteps'],
#                 resultReportingFormatting = content['resultReportingFormatting'],
#                 dateLastUpdate = str(datetime.date.today())
#                 )
#
#             core_obj.save()
#
#             # Save Partner form
#
#             # Checkbox value is not posted if checkbox is not ticked! Check for this.
#             lead = False
#             if 'lead' in content.keys():
#                 lead = True
#
#             partnerObj = Partner(
#                 dataset = core_obj,
#                 name=content['name'],
#                 email=content['email'],
#                 lead=lead
#                 )
#
#             partnerObj.save()
#
#             return HttpResponseRedirect(
#                 reverse('protocoltool:detail')
#             )
#         else:
#             # User is redirected to main page
#             return HttpResponseRedirect(reverse('protocoltool:detail'))
#
#     elif request.method == 'GET':
#
#         core_obj = BasicDataset(
#             title='Title of the protocol'
#             )
#         core_obj.save()
#
#         coreData = BasicDataset.objects.get(id=core_obj.id)
#         formCore = BasicDatasetForm(instance=coreData)
#         formPartner = PartnerForm()
#
#         formList = [
#             ['Basic', formCore],
#             ['Partner', formPartner],
#         ]
#
#         context = {
#             'dataset_id': core_obj.id,
#             'edit': True,
#             'forms_list': formList,
#             'existingPartnersJSON': json.dumps([])
#         }
#
#         return render(request, 'protocoltool/form.html', context)