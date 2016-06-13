from django.conf.urls import patterns, url

from protocoltool import views

urlpatterns = patterns('',
    # Ex: /project/ (No project selected)
    url(r'^$', views.detail, name='detail'),
    # Ex: /project/1/ (Project selected)
    url(r'^(?P<project_id>\d*)/$', views.detail, name='detail'),
    # Ex: /project/1/form/ (Form to choose dataset template and add dataset to project)
    #url(r'^(?P<project_id>\d*)/form/$', views.form_dataset, name='form'),
    url(r'^form/$', views.form_dataset, name='form'),
    # Ex: /project/1/form/2/ (edit existing dataset)
    #url(r'^(?P<project_id>\d*)/form/(?P<dataset_id>\d*)/$', views.edit_dataset, name='edit_dataset'),
    url(r'^form/(?P<dataset_id>\d*)/$', views.edit_dataset, name='edit_dataset'),
)