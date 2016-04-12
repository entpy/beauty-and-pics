from django.conf.urls import url
from custom_form_app import views

urlpatterns = [
    url(r'^$', views.ajax_action, name='ajax_action'),
]
