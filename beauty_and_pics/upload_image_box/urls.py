from django.conf.urls import patterns, url
from upload_image_box import views

urlpatterns = patterns('',
    url(r'^upload/', views.upload, name='upload'),
    url(r'^crop/', views.crop, name='crop'),
)
