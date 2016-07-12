__author__ = 'beekhuiz'
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting

def createPartnerModelFromClient(postDict, update):
    '''
    Creates a new data Partner model object using an AJAX call from the client
    :param postDict: information of the Partner from the client
    :param update: boolean indicating whether it is an update or an addition
    :return: none
    '''

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
    '''
    Store all partner information in an array list
    :param datasetID: id of the dataset for which the partners are retrieved
    :return: list with all partners
    '''

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

    '''
    Creates a new data preparation model object using an AJAX call from the client
    :param postDict: information of the Data&Method preparation part from the client
    :param update: boolean indicating whether it is an update or an addition
    :return: none
    '''

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
            task=postDict['task'],
            description=postDict['description'],
            partner = partner,
            deadline=postDict['deadline'],
            done=done
            )
    else:
        # create new request object
        reqObj = DataReq(
            dataset = dataset,
            task=postDict['task'],
            description=postDict['description'],
            partner = partner,
            deadline=postDict['deadline'],
            done=done
            )

        reqObj.save()


def createExpStepModelFromClient(postDict, update):
    '''
    Creates a new data Experiment step model object using an AJAX call from the client
    :param postDict: information of the Experiment Execution step from the client
    :param update: boolean indicating whether it is an update or an addition
    :return: none
    '''

    dataset = BasicDataset.objects.get(id=postDict['datasetID'])
    partner = Partner.objects.get(id=postDict['partnerID'])

    if update:
        ExpStep.objects.filter(id=postDict['expStepID']).update(
            dataset = dataset,
            task=postDict['task'],
            properties=postDict['properties'],
            partner = partner,
            deadline=postDict['deadline'],
            )
    else:
        # create new exp step object
        expStepObj = ExpStep(
            dataset = dataset,
            task=postDict['task'],
            properties=postDict['properties'],
            partner = partner,
            deadline=postDict['deadline'],
            )

        expStepObj.save()



def createReportingModelFromClient(postDict, update):
    '''
    Creates a new Result Reporting  model object using an AJAX call from the client
    :param postDict: information of the Result Reporting step from the client
    :param update: boolean indicating whether it is an update or an addition
    :return: none
    '''

    dataset = BasicDataset.objects.get(id=postDict['datasetID'])
    partner = Partner.objects.get(id=postDict['partnerID'])

    if update:
        Reporting.objects.filter(id=postDict['reportingID']).update(
            dataset = dataset,
            task=postDict['task'],
            properties=postDict['properties'],
            partner = partner,
            deadline=postDict['deadline'],
            )
    else:
        # create new exp step object
        reportingObj = Reporting(
            dataset = dataset,
            task=postDict['task'],
            properties=postDict['properties'],
            partner = partner,
            deadline=postDict['deadline'],
            )

        reportingObj.save()


def getReqsList(datasetID):
    '''
    Store all data preparation information in an array list
    :param datasetID: id of the dataset for which the info are retrieved
    :return: list with all data preparation information
    '''

    existingReqs = DataReq.objects.filter(dataset__id=datasetID)

    existingReqsList = []
    for req in existingReqs:
        reqDict = {
            "id": req.id,
            "task": req.task,
            "description": req.description,
            "partnerID": req.partner.id,
            "deadline": str(req.deadline),
            "done": str(req.done),
        }
        existingReqsList.append(reqDict)

    return existingReqsList


def getExpStepsList(datasetID):
    '''
    Store all Experiment Step information in an array list
    :param datasetID: id of the dataset for which the info are retrieved
    :return: list with all Experiment Step information
    '''
    existingExpSteps = ExpStep.objects.filter(dataset__id=datasetID)

    existingExpStepsList = []
    for expStep in existingExpSteps:
        expStepDict = {
            "id": expStep.id,
            "task": expStep.task,
            "properties": expStep.properties,
            "partnerID": expStep.partner.id,
            "deadline": str(expStep.deadline),
        }
        existingExpStepsList.append(expStepDict)

    return existingExpStepsList


def getReportingsList(datasetID):
    '''
    Store all Result Reporting information in an array list
    :param datasetID: id of the dataset for which the info are retrieved
    :return: list with all Result Reporting information
    '''
    existingReportings = Reporting.objects.filter(dataset__id=datasetID)

    existingReportingsList = []
    for reporting in existingReportings:
        reportingDict = {
            "id": reporting.id,
            "task": reporting.task,
            "properties": reporting.properties,
            "partnerID": reporting.partner.id,
            "deadline": str(reporting.deadline),
        }
        existingReportingsList.append(reportingDict)

    return existingReportingsList