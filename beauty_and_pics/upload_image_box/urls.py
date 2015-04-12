from django.conf.urls import patterns, url
from upload_image_box import views

urlpatterns = patterns('',
    url(r'^example/', views.upload_example, name='upload_example'),
)
