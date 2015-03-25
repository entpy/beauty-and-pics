from django.conf.urls import patterns, url
from custom_form_app import views

urlpatterns = patterns('',
    url(r'^$', views.ajax_action, name='ajax_action'),
)
