import os
# Imports for responding
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
# Imports of models
from datetime import datetime
from .forms import BasicDatasetForm, PartnerForm
from .models import BasicDataset, Partner
import json
# from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.utils.safestring import mark_safe

import pdb


# Django exceptions
from django.core.exceptions import ObjectDoesNotExist


def detail(request):

    context = {}

    if request.method == 'POST':
        action = request.POST

        dataset_id = int(action['dataset_id'])
        dataset_obj = BasicDataset.objects.get(id=dataset_id)

        if action['dataset_action'] == 'delete':
            # Remove metadata in database
            BasicDataset.objects.filter(id=dataset_id).delete()

        elif action['dataset_action'] == 'publish':
            # Fill in dataset published field
            if dataset_obj.published is None:
                dataset_obj.published = datetime.now()
                dataset_obj.save()

        elif action['dataset_action'] == 'unpublish':
            # Empty the dataset published field
            if dataset_obj.published is not None:
                dataset_obj.published = None
                dataset_obj.save()

        elif action['dataset_action'] == 'edit':
            # Get core model data
            core_data = BasicDataset.objects.get(id=dataset_id)
            return HttpResponseRedirect(reverse('protocoltool:edit_dataset', kwargs={'dataset_id': dataset_id}))

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


def form_dataset(request):

    context = {}

    if request.method == 'POST':
        content = request.POST

        if 'form_action' in content:
            # A (filled in) form is submitted
            valid_models = True
            # Collect basic form data and validate it
            # formCore = BasicDatasetForm(content, auto_id='id_basic_%s')
            #
            # formPartner = PartnerForm(content, auto_id='id_partner_%s')
            #
            # formList = [
            #     ['Basic', formCore],
            #     ['Partner', formPartner],
            # ]

            # if not formCore.is_valid() or not form_time.is_valid():
            #     valid_models = False

            if valid_models:

                # Save Core form
                core_obj = BasicDataset(
                    title=content['title'],
                    experimentIdea = content['experimentIdea'],
                    hypothesis = content['hypothesis'],
                    researchObjective = content['researchObjective'],
                    principles = content['principles'],
                    dataReqDescription = content['dataReqDescription'],
                    dataReqProperties = content['dataReqProperties'],
                    dataReqContributingPartner = content['dataReqContributingPartner'],
                    dataReqSubmDate = content['dataReqSubmDate'],
                    expExecutionSteps = content['expExecutionSteps'],
                    resultReportingFormatting = content['resultReportingFormatting']
                    )

                core_obj.save()

                # Save Partner form

                # Checkbox value is not posted if checkbox is not ticked! Check for this.
                lead = False
                if 'lead' in content.keys():
                    lead = True

                partnerObj = Partner(
                    dataset = core_obj,
                    name=content['name'],
                    email=content['email'],
                    lead=lead
                    )

                partnerObj.save()

                return HttpResponseRedirect(
                    reverse('protocoltool:detail')
                )
        else:
            # User is redirected to main page
            return HttpResponseRedirect(reverse('protocoltool:detail'))

    elif request.method == 'GET':

        # formCore = BasicDatasetForm(auto_id='id_basic_%s')
        formCore = BasicDatasetForm()
        # formPartner = PartnerForm(auto_id='id_partner_%s')
        formPartner = PartnerForm()

        formList = [
            ['Basic', formCore],
            ['Partner', formPartner],
        ]

        context = {
            'forms_list': formList,
            'existingPartnersJSON': json.dumps([])
        }

        return render(request, 'protocoltool/form.html', context)



def edit_dataset(request, dataset_id="0"):

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

        # existingPartnersJSON = serializers.serialize('json', Partner.objects.filter(dataset__id=dataset_id))

        # Load in all forms
        formPartner = PartnerForm()

        formList = [
            ['Basic', formCore],
            ['Partner', formPartner],
        ]

        context.update({
            'dataset_id': dataset_id,
            'edit': True,
            'existingPartners': existingPartners,   # for filling in the initial list; TODO: make this unnecessary: fill in list with jscript
            'existingPartnersJSON': json.dumps(existingPartnersList), #mark_safe(existingPartnersJSON),#json.dumps(list(existingPartners), cls=DjangoJSONEncoder),
            'forms_list': formList
        })

        return render(request, 'protocoltool/form.html', context)


    elif request.method == 'POST' and dataset_id != 0:
        content = request.POST

        valid_models = True

        # # Collect basic form data and validate it
        # formCore = BasicDatasetForm(content, auto_id='id_basic_%s')
        # form_time = TemporalExtentForm(content, auto_id='id_temporalExtent_%s')
        #
        # forms_list = [
        #     ['Basic', formCore],
        #     ['Temporal Extent', form_time],
        # ]
        #
        # if not formCore.is_valid() or not form_time.is_valid():
        #     valid_models = False


        if valid_models:
            # Update Core form
            core_obj = BasicDataset(
                id=dataset_id,
                title=content['title'],
                experimentIdea = content['experimentIdea'],
                hypothesis = content['hypothesis'],
                researchObjective = content['researchObjective'],
                principles = content['principles'],
                dataReqDescription = content['dataReqDescription'],
                dataReqProperties = content['dataReqProperties'],
                dataReqContributingPartner = content['dataReqContributingPartner'],
                dataReqSubmDate = content['dataReqSubmDate'],
                expExecutionSteps = content['expExecutionSteps'],
                resultReportingFormatting = content['resultReportingFormatting']
            )
            core_obj.save()

            return HttpResponseRedirect(
                reverse('protocoltool:detail'))

    return HttpResponseRedirect(reverse('protocoltool:detail'))
