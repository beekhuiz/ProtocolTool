from django.conf.urls import patterns, url

from protocoltool import views

urlpatterns = patterns('',
    # Ex: /project/ (No project selected)

    # Ex: /project/1/ (Project selected)
    #url(r'^(?P<project_id>\d*)/$', views.protocolOverview, name='detail'),
    # Ex: /project/1/form/ (Form to choose dataset template and add dataset to project)
    #url(r'^(?P<project_id>\d*)/form/$', views.form_dataset, name='form'),

    #url(r'^form/$', views.formBasic, name='formbasic'),
    url(r'^$', views.protocolOverview, name='protocoloverview'),
    url(r'^form/$', views.createProtocol, name='createprotocol'),
    url(r'^form/(?P<dataset_id>\d*)/$', views.formAll, name='formall'),
    url(r'^view/(?P<dataset_id>\d*)/$', views.viewProtocol, name='viewprotocol'),

    url(r'^addpartner/$', views.addPartner, name='add_partner'),
    url(r'^updatepartner/$', views.updatePartner, name='update_partner'),
    url(r'^deletepartner/$', views.deletePartner, name='delete_partner'),
                       
    url(r'^addreq/$', views.addReq, name='add_req'),
    url(r'^updatereq/$', views.updateReq, name='update_req'),
    url(r'^deletereq/$', views.deleteReq, name='delete_req'),

    url(r'^addstep/$', views.addExpStep, name='add_step'),
    url(r'^updatestep/$', views.updateExpStep, name='update_step'),
    url(r'^deletestep/$', views.deleteExpStep, name='delete_step'),

    url(r'^addreporting/$', views.addReporting, name='add_reporting'),
    url(r'^updatereporting/$', views.updateReporting, name='update_reporting'),
    url(r'^deletereporting/$', views.deleteReporting, name='delete_reporting'),
)