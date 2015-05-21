from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # www 
    url(r'^$', 'website.views.www_index', name='www_index'),
    url(r'^index/$', 'website.views.www_index', name='www_index'),
    url(r'^come-funziona/$', 'website.views.www_how_it_works', name='www_how_it_works'),
    url(r'^login/$', 'website.views.www_login', name='www_login'),
    url(r'^logout/$', 'website.views.www_logout', name='www_logout'),
    url(r'^recupera-password/$', 'website.views.www_forgot_password', name='www_forgot_password'),
    url(r'^registrati/$', 'website.views.www_register', name='www_register'),

    # catwalk
    url(r'^passerella/(?:(?P<contest_type>\w+)/)?$', 'website.views.catwalk_index', name='catwalk_index'),
    url(r'^passerella/dettaglio-utente/(?P<user_id>\d+)/$', 'website.views.catwalk_profile', name='catwalk_profile'),
    url(r'^passerella/richiesta-aiuto/$', 'website.views.catwalk_help', name='catwalk_help'),
    url(r'^passerella/segnalazione-utente/(?P<user_id>\d+)/$', 'website.views.catwalk_report_user', name='catwalk_report_user'),

    # private profile
    url(r'^profilo/$', 'website.views.profile_index', name='profile_index'),
    url(r'^profilo/dati-personali/$', 'website.views.profile_data', name='profile_data'),
    url(r'^profilo/preferiti/$', 'website.views.profile_favorites', name='profile_favorites'),
    url(r'^profilo/statistiche/$', 'website.views.profile_stats', name='profile_stats'),
    url(r'^profilo/zona-proibita/$', 'website.views.profile_area51', name='profile_area51'),
    url(r'^profilo/disiscriviti/$', 'website.views.profile_unsubscribe', name='profile_unsubscribe'),

    # email test
    url(r'^email-test/(?P<email_name>\w+)/(?P<email_mode>\w+)/$', 'website.views.email_test', name='email_test'),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # ajax view
    url(r'^ajax/', include('custom_form_app.urls', namespace="custom_form_app")),

    # upload image
    url(r'^upload_image/', include('upload_image_box.urls', namespace="upload_image_box")),
    # upload image example
    # url(r'^example_upload_image/', include('upload_image_box.example.urls', namespace="example_upload_image_box")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL_TMP, document_root=settings.MEDIA_ROOT)
