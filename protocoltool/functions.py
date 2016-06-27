__author__ = 'beekhuiz'
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting

def createPartnerModelFromClient(postDict, update):

    # get the foreign key of the protocol dataset of this partner
    dataset = BasicDataset.objects.get(id=postDict['datasetID'])

    # store the lead as a boolean
    lead = True
    if postDict['lead'] == 'False':
        lead = False

    if update:
        Partner.objects.filter(id=postDict['partnerID']).update(
        name=postDict['name'],
        email=postDict['email'],
        organisation=postDict['organisation'],
        lead=lead)
    else:
        # create new partner object
        partnerObj = Partner(
            dataset = dataset,
            name=postDict['name'],
            email=postDict['email'],
            organisation=postDict['organisation'],
            lead=lead
            )
        partnerObj.save()


def getPartnersList(datasetID):
    # reload all partner information as a array list
    existingPartners = Partner.objects.filter(dataset__id=datasetID)

    existingPartnersList = []
    for partner in existingPartners:
        partnerDict = {
            "id": partner.id,
            "name": partner.name,
            "email": partner.email,
            "organisation": partner.organisation,
            "lead": str(partner.lead),
        }
        existingPartnersList.append(partnerDict)

    return existingPartnersList



def createReqModelFromClient(postDict, update):

    # get the ID of the protocol of this DataRequest
    dataset = BasicDataset.objects.get(id=postDict['datasetID'])
    partner = Partner.objects.get(id=postDict['partnerID'])

    # store the 'done' checkbox as a boolean
    done = True
    if postDict['done'] == 'False':
        done = False

    if update:
        DataReq.objects.filter(id=postDict['reqID']).update(
            dataset = dataset,
            description=postDict['description'],
            properties=postDict['properties'],
            partner = partner,
            deadline=postDict['deadline'],
            done=done
            )
    else:
        # create new request object
        reqObj = DataReq(
            dataset = dataset,
            description=postDict['description'],
            properties=postDict['properties'],
            partner = partner,
            deadline=postDict['deadline'],
            done=done
            )

        reqObj.save()


def createExpStepModelFromClient(postDict, update):

    # get the ID of the protocol of this Exp Step
    dataset = BasicDataset.objects.get(id=postDict['datasetID'])
    partner = Partner.objects.get(id=postDict['partnerID'])

    if update:
        ExpStep.objects.filter(id=postDict['expStepID']).update(
            dataset = dataset,
            description=postDict['description'],
            properties=postDict['properties'],
            partner = partner,
            deadline=postDict['deadline'],
            )
    else:
        # create new exp step object
        expStepObj = ExpStep(
            dataset = dataset,
            description=postDict['description'],
            properties=postDict['properties'],
            partner = partner,
            deadline=postDict['deadline'],
            )

        expStepObj.save()



def createReportingModelFromClient(postDict, update):

    # get the ID of the protocol of this Exp Step
    dataset = BasicDataset.objects.get(id=postDict['datasetID'])
    partner = Partner.objects.get(id=postDict['partnerID'])

    if update:
        Reporting.objects.filter(id=postDict['reportingID']).update(
            dataset = dataset,
            description=postDict['description'],
            properties=postDict['properties'],
            partner = partner,
            deadline=postDict['deadline'],
            )
    else:
        # create new exp step object
        reportingObj = Reporting(
            dataset = dataset,
            description=postDict['description'],
            properties=postDict['properties'],
            partner = partner,
            deadline=postDict['deadline'],
            )

        reportingObj.save()


def getReqsList(datasetID):

    # reload all request information as a array list
    existingReqs = DataReq.objects.filter(dataset__id=datasetID)

    existingReqsList = []
    for req in existingReqs:
        reqDict = {
            "id": req.id,
            "description": req.description,
            "properties": req.properties,
            "partnerID": req.partner.id,
            "deadline": str(req.deadline),
            "done": str(req.done),
        }
        existingReqsList.append(reqDict)

    return existingReqsList


def getExpStepsList(datasetID):

    # reload all exp step information as a array list
    existingExpSteps = ExpStep.objects.filter(dataset__id=datasetID)

    existingExpStepsList = []
    for expStep in existingExpSteps:
        expStepDict = {
            "id": expStep.id,
            "description": expStep.description,
            "properties": expStep.properties,
            "partnerID": expStep.partner.id,
            "deadline": str(expStep.deadline),
        }
        existingExpStepsList.append(expStepDict)

    return existingExpStepsList


def getReportingsList(datasetID):

    # reload all exp step information as a array list
    existingReportings = Reporting.objects.filter(dataset__id=datasetID)

    existingReportingsList = []
    for reporting in existingReportings:
        reportingDict = {
            "id": reporting.id,
            "description": reporting.description,
            "properties": reporting.properties,
            "partnerID": reporting.partner.id,
            "deadline": str(reporting.deadline),
        }
        existingReportingsList.append(reportingDict)

    return existingReportingsList