__author__ = 'beekhuiz'
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting
from django.http import HttpResponse
from io import BytesIO

from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import (
    black,
    blue,
    white,
)

import pdb


def createPDF(datasetID):
    """
    Get the ID of the dataset protocol and creates a PDF of this protocol using the reportlab tools
    :param datasetID:
    :return: a HTTPResponse PDF object
    """

    # Get all the information of this protocol
    basicInfo = BasicDataset.objects.get(id=datasetID)
    partnerInfo = Partner.objects.filter(dataset_id=datasetID)
    reqInfo = DataReq.objects.filter(dataset_id=datasetID)
    stepInfo = ExpStep.objects.filter(dataset_id=datasetID)
    reportingInfo = Reporting.objects.filter(dataset_id=datasetID)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + basicInfo.title + '.pdf'

    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='Times-Roman',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Helvetica',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,
            splitLongWords=1,
        ),
    }

    styles['title1'] = ParagraphStyle(
        'title1',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=42,
        alignment=TA_CENTER,
        textColor=black,
    )

    styles['title2'] = ParagraphStyle(
        'title2',
        parent=styles['default'],
        fontName='Helvetica',
        fontSize=14,
        leading=22,
        alignment=TA_LEFT,
        textColor=black,
    )

    buffer = BytesIO()
    doc = BaseDocTemplate(buffer)

    doc.addPageTemplates(
        [
            PageTemplate(
                frames=[
                    Frame(
                        doc.leftMargin,
                        doc.bottomMargin,
                        doc.width,
                        doc.height,
                        id=None
                    ),
                ]
            ),
        ]
    )

    story = []

    story.append(Paragraph('Protocol: {}'.format(basicInfo.title), styles['title1']))

    story.append(Paragraph('General Information', styles['title2']))
    story.append(Paragraph('Experiment Idea: {}'.format(basicInfo.experimentIdea), styles['default']))
    story.append(Paragraph('Hypothesis: {}'.format(basicInfo.hypothesis), styles['default']))
    story.append(Paragraph('Research objective: {}'.format(basicInfo.researchObjective), styles['default']))
    story.append(Paragraph('Date last update: {}'.format(basicInfo.dateLastUpdate), styles['default']))
    story.append(Spacer(1, 8))

    # Partners
    story.append(Spacer(1, 10))
    story.append(Paragraph('Partners', styles['title2']))

    for partner in partnerInfo:
        if partner.lead == True:
            story.append(Paragraph('Name: {} (lead)'.format(partner.name), styles['default']))
        else:
            story.append(Paragraph('Name: {}'.format(partner.name), styles['default']))

        story.append(Paragraph('E-mail: {}'.format(partner.email), styles['default']))
        story.append(Paragraph('Organisation: {}'.format(partner.organisation), styles['default']))
        story.append(Spacer(1, 8))


    # Data Method preparation
    story.append(Spacer(1, 10))
    story.append(Paragraph('Data & Method Preparation', styles['title2']))

    for req in reqInfo:
        story.append(Paragraph('Description: {}'.format(req.description), styles['default']))
        story.append(Paragraph('Properties: {}'.format(req.properties), styles['default']))
        story.append(Paragraph('Contributing partner: {}'.format(req.partner.name), styles['default']))
        story.append(Paragraph('Deadline: {}'.format(req.deadline), styles['default']))

        if req.done == True:
            story.append(Paragraph('Done: Yes', styles['default']))
        else:
            story.append(Paragraph('Done: No', styles['default']))

        story.append(Spacer(1, 8))


    # Experiment execution step
    story.append(Spacer(1, 10))
    story.append(Paragraph('Experiment Analysis Steps', styles['title2']))

    for step in stepInfo:
        story.append(Paragraph('Description: {}'.format(step.description), styles['default']))
        story.append(Paragraph('Output: {}'.format(step.properties), styles['default']))
        story.append(Paragraph('Contributing partner: {}'.format(step.partner.name), styles['default']))
        story.append(Paragraph('Deadline: {}'.format(step.deadline), styles['default']))

        story.append(Spacer(1, 8))


    # Result reporting
    story.append(Spacer(1, 10))
    story.append(Paragraph('Result Reporting', styles['title2']))

    for reporting in reportingInfo:
        story.append(Paragraph('Description: {}'.format(reporting.description), styles['default']))
        story.append(Paragraph('Output: {}'.format(reporting.properties), styles['default']))
        story.append(Paragraph('Contributing partner: {}'.format(reporting.partner.name), styles['default']))
        story.append(Paragraph('Deadline: {}'.format(reporting.deadline), styles['default']))

        story.append(Spacer(1, 8))


    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
