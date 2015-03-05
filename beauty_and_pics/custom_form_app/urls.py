from django.conf.urls import patterns, url
from custom_form_app import views

urlpatterns = patterns('',
    url(r'^$', views.manage_form, name='manage_form'),
)
